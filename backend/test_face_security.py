import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException

# Mock the database before importing controllers
import app.controllers.face_controller as fc
from app.models.face_models import FaceLoginRequest
from app.services.langchain_auth import LangChainAuthDecisionService, AuthDecisionSchema
from app.services.vector_search import VectorSearchService

class TestFaceSecurity(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Reset mocks
        fc.db = MagicMock()
        fc.db.users = MagicMock()
        fc.db.face_login_attempts = MagicMock()
        fc.db.face_login_attempts.insert_one = AsyncMock()
        fc.db.face_login_attempts.distinct = AsyncMock(return_value=[])
        fc.db.device_trust = MagicMock()
        fc.db.anti_spoofing_logs = MagicMock()
        fc.db.anti_spoofing_logs.find_one = AsyncMock(return_value=None)

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_login_face_requires_email(self, mock_langchain, mock_vector, mock_analysis):
        # Arrange
        payload = FaceLoginRequest(
            email="",
            frame="base64string",
            device_fingerprint="test-device"
        )
        response = MagicMock()
        request = MagicMock()
        request.client = MagicMock()
        request.client.host = "127.0.0.1"

        # Act & Assert
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(payload, response, request)
        self.assertEqual(ctx.exception.status_code, 400)
        self.assertIn("Email address is required", ctx.exception.detail)

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_login_face_user_not_found(self, mock_langchain, mock_vector, mock_analysis):
        # Arrange
        payload = FaceLoginRequest(
            email="nonexistent@company.com",
            frame="base64string",
            device_fingerprint="test-device"
        )
        response = MagicMock()
        request = MagicMock()
        request.client = MagicMock()
        request.client.host = "127.0.0.1"

        fc.db.users.find_one = AsyncMock(return_value=None)

        # Act & Assert
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(payload, response, request)
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("Biometric credentials match failed", ctx.exception.detail)

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_login_face_not_registered(self, mock_langchain, mock_vector, mock_analysis):
        # Arrange
        payload = FaceLoginRequest(
            email="unregistered@company.com",
            frame="base64string",
            device_fingerprint="test-device"
        )
        response = MagicMock()
        request = MagicMock()
        request.client = MagicMock()
        request.client.host = "127.0.0.1"

        user_doc = {"user_id": "user123", "email": "unregistered@company.com", "face_registered": False}
        fc.db.users.find_one = AsyncMock(return_value=user_doc)

        # Act & Assert
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(payload, response, request)
        self.assertEqual(ctx.exception.status_code, 403)
        self.assertIn("Face ID not registered", ctx.exception.detail)

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_login_face_strict_1to1_filter_passed_to_search(self, mock_langchain, mock_vector, mock_analysis):
        # Arrange
        payload = FaceLoginRequest(
            email="user@company.com",
            frame="base64string",
            device_fingerprint="test-device"
        )
        response = MagicMock()
        request = MagicMock()
        request.client = MagicMock()
        request.client.host = "127.0.0.1"

        user_doc = {"user_id": "user123", "email": "user@company.com", "face_registered": True}
        fc.db.users.find_one = AsyncMock(return_value=user_doc)
        
        # Mock face analyzer to detect face
        mock_analysis.base64_to_image.return_value = MagicMock()
        mock_analysis.analyze_face.return_value = {"ear": {"avg": 0.3}, "pose": {}, "smile": 0.0, "crop_box": (0, 0, 10, 10)}
        mock_analysis.generate_face_embedding.return_value = [0.1] * 512
        mock_analysis._get_ort_session.return_value = True # ArcFace ONNX active

        # Mock vector search to return a hit
        mock_vector.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "user123", "similarity": 0.85, "metadata": {}}
        ])

        # Mock langchain decision to allow
        mock_langchain.evaluate_auth_request = AsyncMock(return_value=AuthDecisionSchema(
            decision="ALLOW",
            confidence_score=0.85,
            liveness_valid=True,
            threat_detected=False,
            reasoning="Valid face ID match"
        ))

        fc.db.face_login_attempts.count_documents = AsyncMock(return_value=0)
        fc.db.device_trust.find_one = AsyncMock(return_value=None)
        fc.db.device_trust.update_one = AsyncMock()
        fc.db.users.update_one = AsyncMock()
        fc.db.face_login_attempts.insert_one = AsyncMock()
        
        with patch("app.controllers.face_controller.generate_token") as mock_gen_token:
            # Act
            res = await fc.FaceController.login_face(payload, response, request)
            
            # Assert
            self.assertTrue(res["success"])
            # Verify 1-1 search was enforced by passing matched_user_id
            mock_vector.search_nearest_neighbors.assert_called_once_with(
                [0.1] * 512, limit=5, user_id="user123"
            )

    @patch("app.controllers.face_controller.FaceAnalysisService")
    @patch("app.controllers.face_controller.VectorSearchService")
    @patch("app.controllers.face_controller.LangChainAuthDecisionService")
    async def test_login_face_denied_below_threshold(self, mock_langchain, mock_vector, mock_analysis):
        # Arrange
        payload = FaceLoginRequest(
            email="user@company.com",
            frame="base64string",
            device_fingerprint="test-device"
        )
        response = MagicMock()
        request = MagicMock()
        request.client = MagicMock()
        request.client.host = "127.0.0.1"

        user_doc = {"user_id": "user123", "email": "user@company.com", "face_registered": True}
        fc.db.users.find_one = AsyncMock(return_value=user_doc)
        
        mock_analysis.base64_to_image.return_value = MagicMock()
        mock_analysis.analyze_face.return_value = {"ear": {"avg": 0.3}, "pose": {}, "smile": 0.0, "crop_box": (0, 0, 10, 10)}
        mock_analysis.generate_face_embedding.return_value = [0.1] * 512
        mock_analysis._get_ort_session.return_value = True # ArcFace ONNX active

        # Low similarity hit (0.50 similarity is below ArcFace threshold 0.72)
        mock_vector.search_nearest_neighbors = AsyncMock(return_value=[
            {"userId": "user123", "similarity": 0.50, "metadata": {}}
        ])

        # Act & Assert
        with self.assertRaises(HTTPException) as ctx:
            await fc.FaceController.login_face(payload, response, request)
        self.assertEqual(ctx.exception.status_code, 401)
        self.assertIn("Biometric credentials match failed", ctx.exception.detail)


if __name__ == "__main__":
    unittest.main()
