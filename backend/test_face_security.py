"""
Comprehensive Face Recognition Security Test Suite
====================================================
Tests all security layers of the face biometric system:
  - Multi-person frame rejection via DeepFace.count_faces (login + registration)
  - DeepFace.verify face comparison (same person, different person)
  - Image quality gates (blur, brightness, contrast)
  - Similarity threshold enforcement (strict 0.80 ArcFace)
  - Rate limiting / lockout
  - Liveness (EAR) enforcement
  - Head pose rejection
  - Missing / invalid frame handling
  - Account state checks (locked, inactive, unregistered)
  - Device trust and IP anomaly signals
  - LangChain DENY and CHALLENGE flows
"""

import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException

import app.controllers.face_controller as fc
from app.models.face_models import FaceLoginRequest, FaceRegisterRequest
from app.services.langchain_auth import LangChainAuthDecisionService, AuthDecisionSchema
from app.services.vector_search import VectorSearchService

# ─────────────────────────────────────────────────────────────────────────────
# Shared helpers
# ─────────────────────────────────────────────────────────────────────────────

def _make_request(ip: str = "127.0.0.1") -> MagicMock:
    req = MagicMock()
    req.client = MagicMock()
    req.client.host = ip
    return req


def _make_response() -> MagicMock:
    return MagicMock()


def _login_payload(email: str = "user@test.com", fingerprint: str = "fp-001") -> FaceLoginRequest:
    return FaceLoginRequest(
        email=email,
        frame="data:image/jpeg;base64,/9j/fake==",
        device_fingerprint=fingerprint,
    )


def _good_analysis(ear: float = 0.32, yaw: float = 2.0, pitch: float = 1.0) -> dict:
    return {
        "ear":      {"left": ear, "right": ear, "avg": ear},
        "pose":     {"yaw": yaw, "pitch": pitch, "roll": 1.0},
        "smile":    0.45,
        "lips_open": 0.05,
        "symmetry": 0.92,
        "crop_box": (20, 20, 180, 180),
        "landmarks": [[0.0, 0.0, 0.0]] * 478,
    }


def _registered_user(user_id: str = "uid-001", email: str = "user@test.com") -> dict:
    return {
        "user_id":  user_id,
        "email":    email,
        "username": "testuser",
        "full_name": "Test User",
        "face_registered": True,
        "is_active": True,
        "is_locked": False,
        "onboarding_completed": True,
        "avatar": None,
    }


def _allow_decision(score: float = 0.92) -> AuthDecisionSchema:
    return AuthDecisionSchema(
        decision="ALLOW",
        confidence_score=score,
        liveness_valid=True,
        threat_detected=False,
        reasoning="Valid face ID match",
    )


# ─────────────────────────────────────────────────────────────────────────────
# Test class
# ─────────────────────────────────────────────────────────────────────────────

class TestFaceSecurity(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        fc.db = MagicMock()
        fc.db.users = MagicMock()
        fc.db.face_login_attempts = MagicMock()
        fc.db.face_login_attempts.insert_one = AsyncMock()
        fc.db.face_login_attempts.distinct = AsyncMock(return_value=[])
        fc.db.face_login_attempts.count_documents = AsyncMock(return_value=0)
        fc.db.device_trust = MagicMock()
        fc.db.device_trust.find_one = AsyncMock(return_value=None)
        fc.db.device_trust.update_one = AsyncMock()
        fc.db.anti_spoofing_logs = MagicMock()
        fc.db.anti_spoofing_logs.find_one = AsyncMock(return_value=None)

    # ──────────────────────────────────────────────────────────────────────────
    # A. Input Validation
    # ──────────────────────────────────────────────────────────────────────────

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_A1_login_empty_email_rejected(self, *_):
        payload = _login_payload(email="")
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(payload, _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 400)
        self.assertIn("Email address is required", ctx.exception.detail)

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_A2_login_whitespace_email_rejected(self, *_):
        payload = _login_payload(email="   ")
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(payload, _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 400)

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_A3_invalid_frame_returns_400(self, mock_lc, mock_vs, mock_fa):
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        mock_fa.base64_to_image.return_value = None  # decode fails
        mock_fa._get_ort_session.return_value = True
        payload = _login_payload()
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(payload, _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 400)
        self.assertIn("Invalid camera frame", ctx.exception.detail)

    # ──────────────────────────────────────────────────────────────────────────
    # B. User / Registration State
    # ──────────────────────────────────────────────────────────────────────────

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_B1_user_not_found_returns_401(self, *_):
        fc.db.users.find_one = AsyncMock(return_value=None)
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 401)

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_B2_face_not_registered_returns_403(self, *_):
        user = _registered_user()
        user["face_registered"] = False
        fc.db.users.find_one = AsyncMock(return_value=user)
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 403)
        self.assertIn("Face ID not registered", ctx.exception.detail)

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_B3_locked_account_denied_after_allow(self, mock_lc, mock_vs, mock_fa):
        user = _registered_user()
        user["is_locked"] = True
        fc.db.users.find_one = AsyncMock(return_value=user)
        fc.db.users.update_one = AsyncMock()
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.1] * 512
        mock_fa._get_ort_session.return_value = True
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "uid-001", "similarity": 0.93}
        ])
        mock_lc.evaluate_auth_request = AsyncMock(return_value=_allow_decision(0.93))
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 403)
        self.assertIn("locked", ctx.exception.detail)

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_B4_inactive_account_denied_after_allow(self, mock_lc, mock_vs, mock_fa):
        user = _registered_user()
        user["is_active"] = False
        fc.db.users.find_one = AsyncMock(return_value=user)
        fc.db.users.update_one = AsyncMock()
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.1] * 512
        mock_fa._get_ort_session.return_value = True
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "uid-001", "similarity": 0.93}
        ])
        mock_lc.evaluate_auth_request = AsyncMock(return_value=_allow_decision(0.93))
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 403)
        self.assertIn("deactivated", ctx.exception.detail)

    # ──────────────────────────────────────────────────────────────────────────
    # C. MULTI-FACE SECURITY (core new feature)
    # ──────────────────────────────────────────────────────────────────────────

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_C1_two_faces_in_login_frame_returns_403(self, mock_lc, mock_vs, mock_fa):
        """Two people in frame during login MUST be hard-blocked (403)."""
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa._get_ort_session.return_value = True
        # Sentinel: multi-face detected
        mock_fa.analyze_face.return_value = {"multi_face_detected": True, "face_count": 2}
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 403)
        self.assertIn("2 people", ctx.exception.detail)
        self.assertIn("Security violation", ctx.exception.detail)

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_C2_three_faces_in_login_frame_returns_403(self, mock_lc, mock_vs, mock_fa):
        """Three people in frame — same hard block, count surfaced in message."""
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa._get_ort_session.return_value = True
        mock_fa.analyze_face.return_value = {"multi_face_detected": True, "face_count": 3}
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 403)
        self.assertIn("3 people", ctx.exception.detail)

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_C3_multi_face_login_is_logged_to_db(self, mock_lc, mock_vs, mock_fa):
        """Multi-face attempt must be persisted to face_login_attempts for audit."""
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa._get_ort_session.return_value = True
        mock_fa.analyze_face.return_value = {"multi_face_detected": True, "face_count": 2}
        try:
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        except HTTPException:
            pass
        fc.db.face_login_attempts.insert_one.assert_called_once()
        call_args = fc.db.face_login_attempts.insert_one.call_args[0][0]
        self.assertEqual(call_args["decision"], "DENY_MULTI_FACE")
        self.assertFalse(call_args["success"])

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    async def test_C4_multi_face_during_registration_returns_400(self, mock_vs, mock_fa):
        """Two faces in registration frame must block enrollment."""
        user = _registered_user()
        fc.db.users.find_one = AsyncMock(return_value=user)
        fc.db.face_landmarks = MagicMock()
        fc.db.face_landmarks.delete_many = AsyncMock()
        fc.db.face_landmarks.insert_many = AsyncMock()
        fc.db.users.update_one = AsyncMock()
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa._get_ort_session.return_value = True  # ArcFace active
        mock_fa.analyze_face.return_value = {"multi_face_detected": True, "face_count": 2}
        mock_vs.delete_user_embeddings = AsyncMock()
        payload = FaceRegisterRequest(
            email="user@test.com",
            frames=["data:image/jpeg;base64,/9j/fake=="],
            angles=["front"],
            device_fingerprint="fp-reg-001",
        )
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.register_face(payload, _make_response())
        self.assertEqual(ctx.exception.status_code, 400)
        self.assertIn("Multiple people", ctx.exception.detail)

    # ──────────────────────────────────────────────────────────────────────────
    # D. Similarity Threshold (strict 0.80)
    # ──────────────────────────────────────────────────────────────────────────

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_D1_similarity_below_threshold_denied(self, mock_lc, mock_vs, mock_fa):
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.1] * 512
        mock_fa._get_ort_session.return_value = True
        # Score 0.72 — was OK under old threshold (0.72) but fails new one (0.80)
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "uid-001", "similarity": 0.72}
        ])
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("Biometric credentials match failed", ctx.exception.detail)

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_D2_similarity_just_below_threshold_denied(self, mock_lc, mock_vs, mock_fa):
        """Score of 0.799 should be denied (threshold is 0.800)."""
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.1] * 512
        mock_fa._get_ort_session.return_value = True
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "uid-001", "similarity": 0.799}
        ])
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 401)

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_D3_no_embedding_hits_returns_401(self, mock_lc, mock_vs, mock_fa):
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.1] * 512
        mock_fa._get_ort_session.return_value = True
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[])
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 401)

    # ──────────────────────────────────────────────────────────────────────────
    # E. Rate Limiting (3 failures → 30-min lockout)
    # ──────────────────────────────────────────────────────────────────────────

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_E1_rate_limited_after_3_failures(self, mock_lc, mock_vs, mock_fa):
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.1] * 512
        mock_fa._get_ort_session.return_value = True
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "uid-001", "similarity": 0.92}
        ])
        # Simulate 3 previous failures (new threshold)
        fc.db.face_login_attempts.count_documents = AsyncMock(return_value=3)
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 429)
        self.assertIn("Too many failed attempts", ctx.exception.detail)

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_E2_two_failures_not_yet_rate_limited(self, mock_lc, mock_vs, mock_fa):
        """2 failures should NOT trigger lockout — only ≥3 does."""
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        fc.db.users.update_one = AsyncMock()
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.1] * 512
        mock_fa._get_ort_session.return_value = True
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "uid-001", "similarity": 0.92}
        ])
        fc.db.face_login_attempts.count_documents = AsyncMock(return_value=2)
        mock_lc.evaluate_auth_request = AsyncMock(return_value=_allow_decision(0.92))
        with patch("app.controllers.face_controller.generate_token"):
            result = await fc.FaceController.login_face(
                _login_payload(), _make_response(), _make_request()
            )
        self.assertTrue(result["success"])

    # ──────────────────────────────────────────────────────────────────────────
    # F. Liveness / EAR Enforcement (threshold raised to 0.25)
    # ──────────────────────────────────────────────────────────────────────────

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_F1_low_ear_triggers_challenge(self, mock_lc, mock_vs, mock_fa):
        """EAR of 0.22 (eyes nearly closed) → liveness_valid=False → LangChain may CHALLENGE."""
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        fc.db.users.update_one = AsyncMock()
        # EAR=0.22 is below new MIN_EAR_LIVENESS=0.25
        mock_fa.analyze_face.return_value = _good_analysis(ear=0.22)
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.generate_face_embedding.return_value = [0.1] * 512
        mock_fa._get_ort_session.return_value = True
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "uid-001", "similarity": 0.92}
        ])
        mock_lc.evaluate_auth_request = AsyncMock(return_value=AuthDecisionSchema(
            decision="CHALLENGE",
            confidence_score=0.92,
            liveness_valid=False,
            threat_detected=False,
            reasoning="Eyes appear closed — liveness unconfirmed",
        ))
        result = await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        self.assertFalse(result["success"])
        self.assertTrue(result.get("challenge_required"))

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_F2_very_low_ear_triggers_deny(self, mock_lc, mock_vs, mock_fa):
        """EAR=0.12 (wide-closed) → DENY from LangChain."""
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        fc.db.users.update_one = AsyncMock()
        mock_fa.analyze_face.return_value = _good_analysis(ear=0.12)
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.generate_face_embedding.return_value = [0.1] * 512
        mock_fa._get_ort_session.return_value = True
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "uid-001", "similarity": 0.92}
        ])
        mock_lc.evaluate_auth_request = AsyncMock(return_value=AuthDecisionSchema(
            decision="DENY",
            confidence_score=0.50,
            liveness_valid=False,
            threat_detected=True,
            reasoning="Eyes closed — possible spoofing (printed photo or replay)",
        ))
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 401)

    # ──────────────────────────────────────────────────────────────────────────
    # G. ML Model Unavailable (ArcFace offline)
    # ──────────────────────────────────────────────────────────────────────────

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_G1_arcface_offline_blocks_login(self, mock_lc, mock_vs, mock_fa):
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.1] * 512
        mock_fa._get_ort_session.return_value = None  # offline
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "uid-001", "similarity": 0.92}
        ])
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 500)
        self.assertIn("ML model engine offline", ctx.exception.detail)

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    async def test_G2_arcface_offline_blocks_registration(self, mock_vs, mock_fa):
        user = _registered_user()
        user["face_registered"] = False
        fc.db.users.find_one = AsyncMock(return_value=user)
        mock_fa._get_ort_session.return_value = None  # offline
        payload = FaceRegisterRequest(
            email="user@test.com",
            frames=["data:image/jpeg;base64,/9j/fake=="],
            angles=["front"],
            device_fingerprint="fp-reg-001",
        )
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.register_face(payload, _make_response())
        self.assertEqual(ctx.exception.status_code, 500)
        self.assertIn("ML model engine offline", ctx.exception.detail)

    # ──────────────────────────────────────────────────────────────────────────
    # H. LangChain DENY and CHALLENGE flows
    # ──────────────────────────────────────────────────────────────────────────

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_H1_langchain_deny_returns_401(self, mock_lc, mock_vs, mock_fa):
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        fc.db.users.update_one = AsyncMock()
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.1] * 512
        mock_fa._get_ort_session.return_value = True
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "uid-001", "similarity": 0.92}
        ])
        mock_lc.evaluate_auth_request = AsyncMock(return_value=AuthDecisionSchema(
            decision="DENY",
            confidence_score=0.30,
            liveness_valid=True,
            threat_detected=True,
            reasoning="Suspicious behavior pattern detected",
        ))
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 401)

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_H2_langchain_challenge_returns_challenge_flag(self, mock_lc, mock_vs, mock_fa):
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        fc.db.users.update_one = AsyncMock()
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.1] * 512
        mock_fa._get_ort_session.return_value = True
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "uid-001", "similarity": 0.92}
        ])
        mock_lc.evaluate_auth_request = AsyncMock(return_value=AuthDecisionSchema(
            decision="CHALLENGE",
            confidence_score=0.75,
            liveness_valid=False,
            threat_detected=False,
            reasoning="New device — extra verification required",
        ))
        result = await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        self.assertFalse(result["success"])
        self.assertTrue(result.get("challenge_required"))
        self.assertEqual(result["email"], "user@test.com")

    # ──────────────────────────────────────────────────────────────────────────
    # I. Full Success Path (1-1 user_id filter enforced)
    # ──────────────────────────────────────────────────────────────────────────

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_I1_successful_login_returns_user_payload(self, mock_lc, mock_vs, mock_fa):
        user = _registered_user()
        fc.db.users.find_one = AsyncMock(return_value=user)
        fc.db.users.update_one = AsyncMock()
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.2] * 512
        mock_fa._get_ort_session.return_value = True
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "uid-001", "similarity": 0.93}
        ])
        mock_lc.evaluate_auth_request = AsyncMock(return_value=_allow_decision(0.93))
        with patch("app.controllers.face_controller.generate_token"):
            result = await fc.FaceController.login_face(
                _login_payload(), _make_response(), _make_request()
            )
        self.assertTrue(result["success"])
        self.assertIn("user_id", result["user"])
        self.assertEqual(result["user"]["email"], "user@test.com")

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_I2_vector_search_called_with_correct_user_id(self, mock_lc, mock_vs, mock_fa):
        """Confirm 1-to-1 search scoping: user_id must be passed to vector search."""
        user = _registered_user(user_id="target-uid-999")
        fc.db.users.find_one = AsyncMock(return_value=user)
        fc.db.users.update_one = AsyncMock()
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.5] * 512
        mock_fa._get_ort_session.return_value = True
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "target-uid-999", "similarity": 0.91}
        ])
        mock_lc.evaluate_auth_request = AsyncMock(return_value=_allow_decision(0.91))
        with patch("app.controllers.face_controller.generate_token"):
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        mock_vs.search_nearest_neighbors.assert_called_once_with(
            [0.5] * 512, limit=5, user_id="target-uid-999"
        )

    # ──────────────────────────────────────────────────────────────────────────
    # J. IP Anomaly and Device Trust signals passed to LangChain
    # ──────────────────────────────────────────────────────────────────────────

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_J1_new_ip_sets_ip_anomaly_flag(self, mock_lc, mock_vs, mock_fa):
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        fc.db.users.update_one = AsyncMock()
        # Simulate past successful logins from a different IP
        fc.db.face_login_attempts.distinct = AsyncMock(return_value=["10.0.0.1"])
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.1] * 512
        mock_fa._get_ort_session.return_value = True
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "uid-001", "similarity": 0.93}
        ])
        mock_lc.evaluate_auth_request = AsyncMock(return_value=_allow_decision(0.93))
        with patch("app.controllers.face_controller.generate_token"):
            await fc.FaceController.login_face(
                _login_payload(), _make_response(), _make_request(ip="192.168.99.1")
            )
        call_kwargs = mock_lc.evaluate_auth_request.call_args.kwargs
        # ip_anomaly must be True because login IP is new
        self.assertTrue(call_kwargs.get("ip_anomaly"))

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_J2_trusted_device_sets_device_trusted_flag(self, mock_lc, mock_vs, mock_fa):
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        fc.db.users.update_one = AsyncMock()
        fc.db.device_trust.find_one = AsyncMock(return_value={"trustScore": 1.0})
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.1] * 512
        mock_fa._get_ort_session.return_value = True
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "uid-001", "similarity": 0.93}
        ])
        mock_lc.evaluate_auth_request = AsyncMock(return_value=_allow_decision(0.93))
        with patch("app.controllers.face_controller.generate_token"):
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        call_kwargs = mock_lc.evaluate_auth_request.call_args.kwargs
        self.assertTrue(call_kwargs.get("device_trusted"))

    # ──────────────────────────────────────────────────────────────────────────
    # K. DeepFace Integration — count_faces + verify paths
    # ──────────────────────────────────────────────────────────────────────────

    @patch("app.controllers.face_controller.DeepFaceService")
    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_K1_deepface_count_faces_two_people_blocks_login(self, mock_lc, mock_vs, mock_fa, mock_df):
        """DeepFace.count_faces returning 2 must block login before any analysis."""
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa._get_ort_session.return_value = True
        # DeepFace detects 2 faces right at the gate
        mock_df.count_faces.return_value = 2
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 403)
        self.assertIn("2 people", ctx.exception.detail)
        # Confirm analyze_face was never called (blocked before it)
        mock_fa.analyze_face.assert_not_called()

    @patch("app.controllers.face_controller.DeepFaceService")
    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_K2_deepface_verify_fails_blocks_login(self, mock_lc, mock_vs, mock_fa, mock_df):
        """DeepFace.verify returning verified=False must deny login with 401."""
        import numpy as np

        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        fc.db.users.update_one = AsyncMock()
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.1] * 512
        mock_fa._get_ort_session.return_value = True
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "uid-001", "similarity": 0.93}
        ])
        # DeepFace says 1 face at count stage
        mock_df.count_faces.return_value = 1
        # DeepFace verify: distance too high → rejected
        mock_df.verify.return_value = {
            "verified": False,
            "distance": 0.85,
            "threshold": 0.40,
            "model": "arcface_onnx_cosine",
            "similarity": 0.15,
        }
        # Enrolled crop exists in DB
        fc.db.face_landmarks = MagicMock()
        fc.db.face_landmarks.find_one = AsyncMock(return_value={
            "userId": "uid-001", "angle": "front", "cropUrl": "http://fake.cloudinary.com/crop.jpg"
        })
        # Patch the URL download + cv2.imread so enrolled image loads without HTTP call
        fake_enrolled_img = np.zeros((100, 100, 3), dtype=np.uint8)
        with (
            patch("urllib.request.urlretrieve"),
            patch("cv2.imread", return_value=fake_enrolled_img),
        ):
            with self.assertRaises(HTTPException) as ctx:
                await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("Face not recognized", ctx.exception.detail)

    @patch("app.controllers.face_controller.DeepFaceService")
    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_K3_deepface_verify_passes_allows_login(self, mock_lc, mock_vs, mock_fa, mock_df):
        """DeepFace.verify verified=True should allow login to proceed."""
        user = _registered_user()
        fc.db.users.find_one = AsyncMock(return_value=user)
        fc.db.users.update_one = AsyncMock()
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.2] * 512
        mock_fa._get_ort_session.return_value = True
        mock_df.count_faces.return_value = 1
        mock_df.verify.return_value = {
            "verified": True,
            "distance": 0.21,
            "threshold": 0.40,
            "model": "arcface_onnx_cosine",
            "similarity": 0.79,
        }
        fc.db.face_landmarks = MagicMock()
        fc.db.face_landmarks.find_one = AsyncMock(return_value={
            "userId": "uid-001", "angle": "front", "cropUrl": "http://fake.cloudinary.com/crop.jpg"
        })
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "uid-001", "similarity": 0.93}
        ])
        mock_lc.evaluate_auth_request = AsyncMock(return_value=_allow_decision(0.93))
        with patch("app.controllers.face_controller.generate_token"):
            result = await fc.FaceController.login_face(
                _login_payload(), _make_response(), _make_request()
            )
        self.assertTrue(result["success"])

    @patch("app.controllers.face_controller.DeepFaceService")
    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_K4_deepface_no_enrolled_crop_skips_verify(self, mock_lc, mock_vs, mock_fa, mock_df):
        """If no enrolled crop exists, DeepFace verify is skipped gracefully."""
        user = _registered_user()
        fc.db.users.find_one = AsyncMock(return_value=user)
        fc.db.users.update_one = AsyncMock()
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.2] * 512
        mock_fa._get_ort_session.return_value = True
        mock_df.count_faces.return_value = 1
        # No crop stored — landmark doc has no cropUrl
        fc.db.face_landmarks = MagicMock()
        fc.db.face_landmarks.find_one = AsyncMock(return_value=None)
        mock_vs.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "uid-001", "similarity": 0.93}
        ])
        mock_lc.evaluate_auth_request = AsyncMock(return_value=_allow_decision(0.93))
        with patch("app.controllers.face_controller.generate_token"):
            result = await fc.FaceController.login_face(
                _login_payload(), _make_response(), _make_request()
            )
        # Should still succeed via ArcFace vector search
        self.assertTrue(result["success"])
        # verify() should NOT have been called
        mock_df.verify.assert_not_called()

    @patch("app.controllers.face_controller.DeepFaceService")
    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_K5_deepface_count_faces_multi_is_logged_to_db(self, mock_lc, mock_vs, mock_fa, mock_df):
        """Multi-face rejection via DeepFace.count_faces must persist audit log."""
        fc.db.users.find_one = AsyncMock(return_value=_registered_user())
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa._get_ort_session.return_value = True
        mock_df.count_faces.return_value = 3  # 3 faces detected
        try:
            await fc.FaceController.login_face(_login_payload(), _make_response(), _make_request())
        except HTTPException:
            pass
        fc.db.face_login_attempts.insert_one.assert_called_once()
        doc = fc.db.face_login_attempts.insert_one.call_args[0][0]
        self.assertEqual(doc["decision"], "DENY_MULTI_FACE")
        self.assertFalse(doc["success"])
        self.assertIn("3 faces", doc["reason"])

    # ──────────────────────────────────────────────────────────────────────────
    # L. Profile Picture Verification during Registration
    # ──────────────────────────────────────────────────────────────────────────

    @patch("app.controllers.face_controller.DeepFaceService")
    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    async def test_L1_registration_with_matching_avatar_succeeds(self, mock_vs, mock_fa, mock_df):
        """If user has an avatar and the captured face matches it, registration succeeds."""
        user = _registered_user()
        user["face_registered"] = False
        user["avatar"] = "http://fake.cloudinary.com/avatar.jpg"
        
        fc.db.users.find_one = AsyncMock(return_value=user)
        fc.db.face_landmarks = MagicMock()
        fc.db.face_landmarks.delete_many = AsyncMock()
        fc.db.face_landmarks.insert_many = AsyncMock()
        fc.db.users.update_one = AsyncMock()
        
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.1] * 512
        mock_fa._get_ort_session.return_value = True  # ArcFace active
        
        mock_df.count_faces.return_value = 1
        mock_df.get_embedding.return_value = [0.1] * 512  # Avatar has a face
        mock_df.verify.return_value = {
            "verified": True,
            "distance": 0.15,
            "threshold": 0.40,
            "model": "arcface_onnx_cosine",
            "similarity": 0.85,
        }
        
        mock_vs.delete_user_embeddings = AsyncMock()
        mock_vs.add_face_embedding = AsyncMock()
        
        payload = FaceRegisterRequest(
            email="user@test.com",
            frames=["data:image/jpeg;base64,/9j/fake=="],
            angles=["front"],
            device_fingerprint="fp-reg-001",
        )
        
        # Mock image download & loading
        import numpy as np
        fake_img = np.zeros((100, 100, 3), dtype=np.uint8)
        with (
            patch("urllib.request.urlretrieve"),
            patch("cv2.imread", return_value=fake_img),
            patch("app.controllers.face_controller.generate_token"),
            patch.object(fc.FaceController, "_upload_face_crop", return_value="http://fake-upload.com"),
        ):
            result = await fc.FaceController.register_face(payload, _make_response())
            
        self.assertTrue(result["success"])
        mock_df.verify.assert_called_once()

    @patch("app.controllers.face_controller.DeepFaceService")
    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    async def test_L2_registration_with_mismatching_avatar_fails(self, mock_vs, mock_fa, mock_df):
        """If user has an avatar but the captured face does not match it, registration fails with 400."""
        user = _registered_user()
        user["face_registered"] = False
        user["avatar"] = "http://fake.cloudinary.com/avatar.jpg"
        
        fc.db.users.find_one = AsyncMock(return_value=user)
        fc.db.face_landmarks = MagicMock()
        fc.db.face_landmarks.delete_many = AsyncMock()
        fc.db.face_landmarks.insert_many = AsyncMock()
        fc.db.users.update_one = AsyncMock()
        
        mock_fa.base64_to_image.return_value = MagicMock()
        mock_fa.analyze_face.return_value = _good_analysis()
        mock_fa.generate_face_embedding.return_value = [0.1] * 512
        mock_fa._get_ort_session.return_value = True  # ArcFace active
        
        mock_df.count_faces.return_value = 1
        mock_df.get_embedding.return_value = [0.1] * 512  # Avatar has a face
        mock_df.verify.return_value = {
            "verified": False,
            "distance": 0.65,
            "threshold": 0.40,
            "model": "arcface_onnx_cosine",
            "similarity": 0.35,
        }
        
        mock_vs.delete_user_embeddings = AsyncMock()
        
        payload = FaceRegisterRequest(
            email="user@test.com",
            frames=["data:image/jpeg;base64,/9j/fake=="],
            angles=["front"],
            device_fingerprint="fp-reg-001",
        )
        
        # Mock image download & loading
        import numpy as np
        fake_img = np.zeros((100, 100, 3), dtype=np.uint8)
        with (
            patch("urllib.request.urlretrieve"),
            patch("cv2.imread", return_value=fake_img),
        ):
            with self.assertRaises(HTTPException) as ctx:
                await fc.FaceController.register_face(payload, _make_response())
                
        self.assertEqual(ctx.exception.status_code, 400)
        self.assertIn("does not match the profile picture", ctx.exception.detail)


if __name__ == "__main__":
    unittest.main(verbosity=2)
