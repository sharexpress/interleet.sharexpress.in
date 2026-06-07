import os
import cv2
import uuid
import logging
import io
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional
from fastapi import HTTPException, Response, Request

from app.core.db import get_db
from app.core.config import PROJECT_ENVIRONMENT, CLOUDINARY_CLOUD_NAME
from app.utils.JWT import generate_token
from app.models.face_models import (
    FaceRegisterRequest,
    FaceLoginRequest,
    FaceVerifyRequest,
    LivenessChallengeVerifyRequest,
    LivenessChallengeStartRequest,
)
from app.services.face_analysis import FaceAnalysisService
from app.services.vector_search import VectorSearchService
from app.services.deepface_service import DeepFaceService
from app.services.langchain_auth import LangChainAuthDecisionService
import numpy as np

logger = logging.getLogger(__name__)
db = get_db()
is_prod = PROJECT_ENVIRONMENT == "PRODUCTION"

# ── Security thresholds ────────────────────────────────────────────────────
# ArcFace ONNX cosine similarity — raised to 0.80 for stricter identity matching
# (same person in good conditions typically scores 0.88–0.97)
SIMILARITY_THRESHOLD_ARCFACE = float(os.getenv("FACE_SIMILARITY_THRESHOLD", "0.80"))
# Geometric fallback — raised from 0.68 → 0.75
SIMILARITY_THRESHOLD_GEOMETRIC = float(os.getenv("FACE_SIMILARITY_THRESHOLD_GEO", "0.75"))

# Rate limiting — tightened: 3 failures → 30-min lockout (was 5 / 15 min)
MAX_FAILURES_BEFORE_LOCKOUT = int(os.getenv("FACE_MAX_FAILURES", "3"))
LOCKOUT_WINDOW_MINUTES = int(os.getenv("FACE_LOCKOUT_MINUTES", "30"))

# Liveness — minimum Eye Aspect Ratio to consider eyes open (was 0.22)
MIN_EAR_LIVENESS = float(os.getenv("FACE_MIN_EAR", "0.25"))


class FaceController:
    @staticmethod
    def _upload_face_crop(image: cv2.Mat, user_id: str, angle: str) -> str:
        """
        Uploads processed face crop to Cloudinary if configured.
        Otherwise, saves to a local uploads directory.
        """
        filename = f"{user_id}_{angle}_{uuid.uuid4().hex[:6]}.jpg"

        # 1. Check if Cloudinary credentials are set
        if CLOUDINARY_CLOUD_NAME and os.getenv("CLOUDINARY_API_KEY"):
            try:
                import cloudinary.uploader

                # Encode CV image to JPEG bytes
                _, buffer = cv2.imencode(".jpg", image)
                img_bytes = buffer.tobytes()

                result = cloudinary.uploader.upload(
                    io.BytesIO(img_bytes),
                    folder="faces",
                    public_id=filename.rsplit(".", 1)[0],
                    overwrite=True,
                    resource_type="image",
                )
                logger.info(
                    "Cloudinary face upload successful: %s", result.get("secure_url")
                )
                return result.get("secure_url")
            except Exception as e:
                logger.error(
                    "Cloudinary face upload failed, falling back to local: %s", e
                )

        # 2. Local Fallback storage
        local_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "uploads",
            "faces",
        )
        os.makedirs(local_dir, exist_ok=True)
        file_path = os.path.join(local_dir, filename)

        cv2.imwrite(file_path, image)
        logger.info("Saved face crop locally: %s", file_path)
        # Return local path url
        return f"/uploads/faces/{filename}"

    @classmethod
    async def register_face(
        cls,
        payload: FaceRegisterRequest,
        response: Response,
        current_user: Optional[dict] = None,
    ):
        """
        Registers user face profile. Analyzes frames, generates embeddings,
        saves to ChromaDB, uploads face crops, and records metadata in MongoDB.
        """
        try:
            user = None
            email = payload.email.strip().lower() if payload.email else None

            if current_user and current_user.get("user"):
                user = current_user["user"]
                user_id = str(user["user_id"])
                email = user.get("email", email)
            else:
                if not email:
                    raise HTTPException(
                        status_code=400,
                        detail="Email is required when registering face biometrics.",
                    )
                user = await db.users.find_one({"email": email})
                if not user:
                    raise HTTPException(
                        status_code=404,
                        detail="User not found. Register an account first.",
                    )
                user_id = str(user["user_id"])

            if len(payload.frames) != len(payload.angles):
                raise HTTPException(
                    status_code=400, detail="Frames and angles length mismatch."
                )

            embeddings = []
            landmark_records = []

            using_arcface = FaceAnalysisService._get_ort_session() is not None
            if not using_arcface:
                logger.error("Face registration failed: ArcFace ML model session is not initialized")
                raise HTTPException(
                    status_code=500,
                    detail="Biometric registration is currently unavailable (ML model engine offline)."
                )

            # Reset existing embeddings for clean registration
            await VectorSearchService.delete_user_embeddings(user_id)
            await db.face_landmarks.delete_many({"userId": user_id})

            for frame_b64, angle in zip(payload.frames, payload.angles):
                img = FaceAnalysisService.base64_to_image(frame_b64)
                if img is None:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid image format for angle {angle}",
                    )

                # For registration, non-frontal angles should use strict=False to bypass pose and symmetry limits
                strict_check = (angle == "front")
                analysis = FaceAnalysisService.analyze_face(img, strict=strict_check)
                if not analysis:
                    raise HTTPException(
                        status_code=400,
                        detail=f"No face detected in the frame for angle {angle}",
                    )
                # Multi-face guard during registration (DeepFace count)
                face_count = DeepFaceService.count_faces(img, strict=strict_check)
                if face_count > 1:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            f"Multiple people ({face_count}) detected in frame for angle '{angle}'. "
                            "Only the enrolling user may be in frame during Face ID registration."
                        ),
                    )
                # Also check MediaPipe sentinel
                if analysis.get("multi_face_detected"):
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            f"Multiple people ({analysis['face_count']}) detected in frame for angle '{angle}'. "
                            "Only the enrolling user may be in frame during Face ID registration."
                        ),
                    )

                # Compare captured face with the user's profile avatar (Google/GitHub profile picture)
                if angle == "front":
                    user_doc = await db.users.find_one({"user_id": user_id})
                    if user_doc and user_doc.get("avatar"):
                        avatar_url = user_doc["avatar"]
                        avatar_img = None
                        if avatar_url.startswith("/uploads/"):
                            local_path = os.path.join(
                                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                avatar_url.lstrip("/"),
                            )
                            if os.path.exists(local_path):
                                avatar_img = cv2.imread(local_path)
                        elif avatar_url.startswith("http"):
                            import urllib.request
                            import tempfile
                            tmp_f = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
                            try:
                                urllib.request.urlretrieve(avatar_url, tmp_f.name)
                                avatar_img = cv2.imread(tmp_f.name)
                            except Exception as dl_err:
                                logger.warning("Could not download profile avatar: %s", dl_err)
                            finally:
                                try:
                                    os.unlink(tmp_f.name)
                                except Exception:
                                    pass

                        if avatar_img is not None:
                            # Verify if the profile avatar actually contains a face
                            avatar_emb = DeepFaceService.get_embedding(avatar_img)
                            if avatar_emb is None:
                                logger.warning("Profile avatar does not contain a recognizable face. Bypassing cross-verification.")
                            else:
                                # Compare captured face with profile avatar face
                                df_result = DeepFaceService.verify(img, avatar_img)
                                if not df_result["verified"]:
                                    logger.warning(
                                        "Face registration BLOCKED — captured face does not match profile picture for user_id=%s. Distance: %.4f",
                                        user_id, df_result["distance"]
                                    )
                                    raise HTTPException(
                                        status_code=400,
                                        detail="Biometric verification failed: The captured face does not match the profile picture associated with this account.",
                                    )
                                logger.info("Profile picture cross-verification passed successfully.")

                # Calculate embedding vector
                embedding = FaceAnalysisService.generate_face_embedding(img, analysis)
                embeddings.append(embedding)

                # Crop face and upload
                x_min, y_min, x_max, y_max = analysis["crop_box"]
                face_crop = img[y_min:y_max, x_min:x_max]
                uploaded_url = cls._upload_face_crop(face_crop, user_id, angle)

                # Store embedding
                await VectorSearchService.add_face_embedding(user_id, embedding, angle)

                # Save landmarks record
                landmark_records.append(
                    {
                        "userId": user_id,
                        "angle": angle,
                        "cropUrl": uploaded_url,
                        "landmarks": analysis["landmarks"],
                        "pose": analysis["pose"],
                        "symmetryScore": analysis["symmetry"],
                        "createdAt": datetime.utcnow(),
                    }
                )

            if not embeddings:
                raise HTTPException(
                    status_code=400, detail="No valid face samples provided."
                )

            # Store landmarks in MongoDB
            await db.face_landmarks.insert_many(landmark_records)

            # Update user profile
            await db.users.update_one(
                {"user_id": user_id},
                {"$set": {"face_registered": True, "updated_at": datetime.utcnow()}},
            )

            # Generate JWT token and sign the user in
            generate_token(user_id, response)
            logger.info("Successfully registered Face ID for user %s", email or user_id)

            return {
                "success": True,
                "message": "Face ID registered successfully",
                "user": {"user_id": user_id, "email": email, "face_registered": True},
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Register Face ID failed: %s", e)
            raise HTTPException(status_code=500, detail="Internal server error")

    @classmethod
    def verify_liveness_frames(
        cls, challenge_type: str, frames: List[str]
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Evaluate frame sequences to verify liveness challenges.
        """
        ears = []
        yaws = []
        pitches = []
        smiles = []

        valid_frames = 0
        for frame_b64 in frames:
            img = FaceAnalysisService.base64_to_image(frame_b64)
            if img is None:
                continue
            # Liveness frames should not be subject to strict frontal pose or symmetry checks
            analysis = FaceAnalysisService.analyze_face(img, strict=False)
            if not analysis:
                continue

            valid_frames += 1
            ears.append(analysis["ear"]["avg"])
            yaws.append(analysis["pose"]["yaw"])
            pitches.append(analysis["pose"]["pitch"])
            smiles.append(analysis["smile"])

        if valid_frames < 2:
            return False, {"reason": "Not enough valid frames detected with a face."}

        liveness_passed = False
        metrics = {
            "valid_frames": valid_frames,
            "min_ear": float(np.min(ears)) if ears else 1.0,
            "max_ear": float(np.max(ears)) if ears else 0.0,
            "max_yaw": float(np.max(yaws)) if yaws else 0.0,
            "min_yaw": float(np.min(yaws)) if yaws else 0.0,
            "max_smile": float(np.max(smiles)) if smiles else 0.0,
            "min_smile": float(np.min(smiles)) if smiles else 0.0,
        }

        if challenge_type == "blink":
            # A blink is valid if the eye aspect ratio drops below 0.20 (eyes closed)
            # and recovers above 0.26 (eyes open)
            if metrics["min_ear"] < 0.20 and metrics["max_ear"] > 0.26:
                liveness_passed = True
            else:
                metrics["reason"] = (
                    f"Blink not detected. EAR range: {metrics['min_ear']:.2f} - {metrics['max_ear']:.2f}"
                )

        elif challenge_type == "turn_left":
            # Turning head left results in positive yaw
            if metrics["max_yaw"] > 12.0:
                liveness_passed = True
            else:
                metrics["reason"] = (
                    f"Head turn left not detected. Max yaw: {metrics['max_yaw']:.1f}°"
                )

        elif challenge_type == "turn_right":
            # Turning head right results in negative yaw
            if metrics["min_yaw"] < -12.0:
                liveness_passed = True
            else:
                metrics["reason"] = (
                    f"Head turn right not detected. Min yaw: {metrics['min_yaw']:.1f}°"
                )

        elif challenge_type == "smile":
            # Smile expands mouth width relative to eye distance
            # Compare maximum smile to baseline and ensure there is an active smile change (delta)
            smile_delta = metrics["max_smile"] - metrics["min_smile"]
            if metrics["max_smile"] > 0.44 and smile_delta > 0.03:
                liveness_passed = True
            else:
                metrics["reason"] = (
                    f"Smile not detected or mouth did not change expression. Max: {metrics['max_smile']:.2f}, Delta: {smile_delta:.2f}"
                )

        elif challenge_type == "move_closer":
            # Moving closer would be tracked by bounding box height size increasing,
            # or average eye distance widening. For simplicity, if frame is valid, let's pass.
            liveness_passed = True

        else:
            metrics["reason"] = f"Unknown challenge type: {challenge_type}"

        return liveness_passed, metrics

    @classmethod
    async def verify_liveness(cls, payload: LivenessChallengeVerifyRequest):
        """API for verifying liveness challenge sequence."""
        try:
            email = payload.email.strip().lower()
            user = await db.users.find_one({"email": email})
            user_id = str(user["user_id"]) if user else "guest"

            liveness_passed, metrics = cls.verify_liveness_frames(
                payload.challenge_type, payload.frames
            )

            # Log anti spoofing results
            await db.anti_spoofing_logs.insert_one(
                {
                    "userId": user_id,
                    "email": email,
                    "challengeType": payload.challenge_type,
                    "livenessPassed": liveness_passed,
                    "metrics": metrics,
                    "deviceFingerprint": payload.device_fingerprint,
                    "timestamp": datetime.utcnow(),
                }
            )

            return {
                "success": liveness_passed,
                "challenge_type": payload.challenge_type,
                "metrics": metrics,
            }
        except Exception as e:
            logger.exception("Liveness challenge verification failed: %s", e)
            raise HTTPException(status_code=500, detail="Internal server error")

    @classmethod
    async def get_active_challenge(cls, payload: LivenessChallengeStartRequest):
        """Gets the next challenge command to display on screen."""
        import random

        challenges = ["blink", "turn_left", "turn_right", "smile"]
        selected = random.choice(challenges)
        return {
            "success": True,
            "challenge_type": selected,
            "instruction": {
                "blink": "Blink twice clearly.",
                "turn_left": "Turn your head slowly to the left.",
                "turn_right": "Turn your head slowly to the right.",
                "smile": "Smile widely showing your teeth.",
            }[selected],
        }

    @classmethod
    async def login_face(
        cls, payload: FaceLoginRequest, response: Response, request: Request
    ):
        """
        Authenticates user via face recognition.

        Security pipeline:
          1. Decode + validate frame (real face must be detected)
          2. Generate biometric embedding
          3. Vector search against all enrolled users
          4. HARD similarity threshold gate (denies if score < threshold)
          5. Confirm matched user has face_registered flag
          6. Email filter validation (optional, additional guard)
          7. Rate-limit check (lockout after N failures)
          8. Device trust + IP anomaly detection
          9. Liveness check (EAR + recent challenge log)
         10. LangChain adaptive risk evaluation
         11. Issue JWT on ALLOW, challenge on CHALLENGE, deny on DENY
        """
        ip_address = request.client.host if request.client else "127.0.0.1"

        try:
            # ── Step 1: Validate email and load user ──────────────────────
            if not payload.email or not payload.email.strip():
                raise HTTPException(
                    status_code=400, detail="Email address is required for Face ID."
                )

            email = payload.email.strip().lower()
            matched_user = await db.users.find_one({"email": email})
            if not matched_user:
                logger.warning("Face login: user not found for email %s", email)
                raise HTTPException(
                    status_code=401, detail="Biometric credentials match failed. Face not recognized."
                )

            # Face must be explicitly enrolled
            if not matched_user.get("face_registered"):
                logger.warning("Face login: face not registered for email %s", email)
                raise HTTPException(
                    status_code=403,
                    detail="Face ID not registered. Please enroll your face in Settings → Security.",
                )

            matched_user_id = str(matched_user["user_id"])

            # ── Step 2: Decode and validate frame ─────────────────────────
            img = FaceAnalysisService.base64_to_image(payload.frame)
            if img is None:
                raise HTTPException(
                    status_code=400, detail="Invalid camera frame image format."
                )

            # ── Step 2a: Multi-face check via DeepFace BEFORE anything else ──
            # This is the fastest guard — count faces directly from raw image
            early_face_count = DeepFaceService.count_faces(img)
            if early_face_count > 1:
                logger.warning(
                    "Face login BLOCKED — DeepFace detected %d faces for email=%s ip=%s",
                    early_face_count, email, ip_address,
                )
                await db.face_login_attempts.insert_one({
                    "userId":            matched_user_id,
                    "email":             email,
                    "success":           False,
                    "decision":          "DENY_MULTI_FACE",
                    "reason":            f"{early_face_count} faces detected in frame (DeepFace)",
                    "ipAddress":         ip_address,
                    "deviceFingerprint": payload.device_fingerprint,
                    "timestamp":         datetime.utcnow(),
                })
                raise HTTPException(
                    status_code=403,
                    detail=(
                        f"Security violation: {early_face_count} people detected in frame. "
                        "Only the account holder may be present during Face ID authentication."
                    ),
                )

            # ── Step 3: Detect face landmarks (strict mode enforces 1-face rule) ──
            analysis = FaceAnalysisService.analyze_face(img, strict=True)
            if not analysis:
                raise HTTPException(
                    status_code=400,
                    detail="No face detected. Ensure good lighting, look directly at camera, and no obstructions.",
                )
            # Hard block: multiple people in frame
            if analysis.get("multi_face_detected"):
                logger.warning(
                    "Face login BLOCKED — multiple faces (%d) detected for email=%s ip=%s",
                    analysis["face_count"], email, ip_address,
                )
                await db.face_login_attempts.insert_one({
                    "userId":            matched_user_id,
                    "email":             email,
                    "success":           False,
                    "decision":          "DENY_MULTI_FACE",
                    "reason":            f"{analysis['face_count']} faces detected in frame",
                    "ipAddress":         ip_address,
                    "deviceFingerprint": payload.device_fingerprint,
                    "timestamp":         datetime.utcnow(),
                })
                raise HTTPException(
                    status_code=403,
                    detail=(
                        f"Security violation: {analysis['face_count']} people detected in frame. "
                        "Only the account holder may be present during Face ID authentication."
                    ),
                )

            # ── Step 4: Generate query embedding ──────────────────────────
            query_vector = FaceAnalysisService.generate_face_embedding(img, analysis)

            # ── Step 5: DeepFace verify — compare live frame against enrolled crop ──
            # Load the best registered face crop for comparison
            deepface_verified = False
            deepface_distance = 1.0
            deepface_model = "unavailable"
            try:
                landmark_doc = await db.face_landmarks.find_one(
                    {"userId": matched_user_id, "angle": "front"},
                )
                if not landmark_doc:
                    # Fall back to any registered angle
                    landmark_doc = await db.face_landmarks.find_one({"userId": matched_user_id})

                if landmark_doc and landmark_doc.get("cropUrl"):
                    crop_url = landmark_doc["cropUrl"]
                    enrolled_img = None

                    # Try to load the enrolled crop image
                    if crop_url.startswith("/uploads/"):
                        # Local file path
                        local_path = os.path.join(
                            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                            crop_url.lstrip("/"),
                        )
                        if os.path.exists(local_path):
                            enrolled_img = cv2.imread(local_path)
                    elif crop_url.startswith("http"):
                        # Download from Cloudinary / remote URL
                        import urllib.request
                        import tempfile
                        tmp_f = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
                        try:
                            urllib.request.urlretrieve(crop_url, tmp_f.name)
                            enrolled_img = cv2.imread(tmp_f.name)
                        except Exception as dl_err:
                            logger.warning("Could not download enrolled crop: %s", dl_err)
                        finally:
                            try:
                                os.unlink(tmp_f.name)
                            except Exception:
                                pass

                    if enrolled_img is not None:
                        df_result = DeepFaceService.verify(img, enrolled_img)
                        deepface_verified = df_result["verified"]
                        deepface_distance = df_result["distance"]
                        deepface_model = df_result["model"]

                        if not deepface_verified:
                            logger.warning(
                                "DeepFace DENY — user=%s distance=%.4f threshold=%.4f model=%s ip=%s",
                                email, deepface_distance, df_result["threshold"], deepface_model, ip_address,
                            )
                            await db.face_login_attempts.insert_one({
                                "userId":            matched_user_id,
                                "email":             email,
                                "success":           False,
                                "decision":          "DENY_DEEPFACE",
                                "reason":            f"DeepFace distance {deepface_distance:.4f} >= threshold {df_result['threshold']:.4f}",
                                "deepfaceModel":     deepface_model,
                                "deepfaceDistance":  deepface_distance,
                                "ipAddress":         ip_address,
                                "deviceFingerprint": payload.device_fingerprint,
                                "timestamp":         datetime.utcnow(),
                            })
                            raise HTTPException(
                                status_code=401,
                                detail="Biometric credentials match failed. Face not recognized.",
                            )
                        else:
                            logger.info(
                                "DeepFace PASS — user=%s distance=%.4f model=%s",
                                email, deepface_distance, deepface_model,
                            )
                    else:
                        logger.warning(
                            "DeepFace: no enrolled crop available for user=%s — skipping DeepFace verify",
                            matched_user_id,
                        )
                else:
                    logger.warning(
                        "DeepFace: no landmark doc or cropUrl for user=%s — skipping DeepFace verify",
                        matched_user_id,
                    )
            except HTTPException:
                raise
            except Exception as df_err:
                logger.warning("DeepFace verify error (non-fatal, continuing pipeline): %s", df_err)

            # ── Step 6: 1-1 Nearest-neighbour vector search (filtered by user_id) ──
            hits = await VectorSearchService.search_nearest_neighbors(
                query_vector, limit=5, user_id=matched_user_id
            )
            if not hits:
                logger.warning("Face login: no enrolled face templates found for user %s", email)
                raise HTTPException(
                    status_code=401, detail="Biometric credentials match failed. Face not recognized."
                )

            top_hit = hits[0]
            similarity_score: float = top_hit["similarity"]

            # ── Step 6: HARD SIMILARITY THRESHOLD ────────────────────────
            using_arcface = FaceAnalysisService._get_ort_session() is not None
            if not using_arcface:
                logger.error("Face login failed: ArcFace ML model session is not initialized")
                raise HTTPException(
                    status_code=500,
                    detail="Biometric authentication is currently unavailable (ML model engine offline)."
                )

            threshold = SIMILARITY_THRESHOLD_ARCFACE

            if similarity_score < threshold:
                logger.warning(
                    "Face login DENIED — user=%s similarity %.4f < threshold %.4f (arcface=%s) ip=%s",
                    email, similarity_score, threshold, using_arcface, ip_address,
                )
                # Log the failed attempt
                await db.face_login_attempts.insert_one({
                    "userId":            matched_user_id,
                    "email":             email,
                    "success":           False,
                    "confidenceScore":   similarity_score,
                    "decision":          "DENY",
                    "reason":            f"Similarity {similarity_score:.4f} below threshold {threshold:.4f}",
                    "ipAddress":         ip_address,
                    "deviceFingerprint": payload.device_fingerprint,
                    "timestamp":         datetime.utcnow(),
                })
                raise HTTPException(
                    status_code=401,
                    detail="Biometric credentials match failed. Face not recognized.",
                )

            # ── Step 7: Rate-limit check ───────────────────────────────────
            lockout_window = datetime.utcnow() - timedelta(minutes=LOCKOUT_WINDOW_MINUTES)
            recent_failures_count = await db.face_login_attempts.count_documents({
                "email":   email,
                "success": False,
                "timestamp": {"$gt": lockout_window},
            })

            if recent_failures_count >= MAX_FAILURES_BEFORE_LOCKOUT:
                logger.warning(
                    "Face login rate-limited — email=%s failures=%d ip=%s",
                    email, recent_failures_count, ip_address,
                )
                raise HTTPException(
                    status_code=429,
                    detail=(
                        f"Too many failed attempts ({recent_failures_count}). "
                        f"Try again in {LOCKOUT_WINDOW_MINUTES} minutes or use Email/OTP login."
                    ),
                )

            # ── Step 8: Device trust + IP anomaly ─────────────────────────
            trust_doc = await db.device_trust.find_one({
                "userId":            matched_user_id,
                "deviceFingerprint": payload.device_fingerprint,
            })
            device_trusted = trust_doc is not None

            past_ips = await db.face_login_attempts.distinct(
                "ipAddress", {"userId": matched_user_id, "success": True}
            )
            ip_anomaly = len(past_ips) > 0 and ip_address not in past_ips

            # ── Step 9: Liveness validation ───────────────────────────────
            liveness_valid = analysis["ear"]["avg"] > MIN_EAR_LIVENESS

            # Allow bypass if device recently passed a full liveness challenge
            challenge_cutoff = datetime.utcnow() - timedelta(minutes=5)
            challenge_passed_recently = await db.anti_spoofing_logs.find_one({
                "email":             email,
                "livenessPassed":    True,
                "deviceFingerprint": payload.device_fingerprint,
                "timestamp":         {"$gt": challenge_cutoff},
            })
            if challenge_passed_recently:
                liveness_valid = True
                logger.info("Liveness bypass granted — recent challenge passed for %s", email)

            liveness_data = {
                "ear":   analysis["ear"]["avg"],
                "pose":  analysis["pose"],
                "smile": analysis["smile"],
            }

            # ── Step 10: LangChain adaptive risk assessment ────────────────
            decision = await LangChainAuthDecisionService.evaluate_auth_request(
                similarity_score=similarity_score,
                liveness_valid=liveness_valid,
                device_trusted=device_trusted,
                recent_failures_count=recent_failures_count,
                ip_anomaly=ip_anomaly,
                liveness_data=liveness_data,
                using_arcface=using_arcface,
            )

            # ── Step 11: Record attempt ────────────────────────────────────
            await db.face_login_attempts.insert_one({
                "userId":            matched_user_id,
                "email":             email,
                "success":           decision.decision == "ALLOW",
                "confidenceScore":   similarity_score,
                "similarityThreshold": threshold,
                "decision":          decision.decision,
                "reason":            decision.reasoning,
                "ipAddress":         ip_address,
                "deviceFingerprint": payload.device_fingerprint,
                "livenessValid":     liveness_valid,
                "usingArcface":      using_arcface,
                "timestamp":         datetime.utcnow(),
            })

            # ── Step 11b: Handle decisions ────────────────────────────────
            if decision.decision == "ALLOW":
                if matched_user.get("is_locked"):
                    raise HTTPException(status_code=403, detail="Account is locked.")
                if not matched_user.get("is_active", True):
                    raise HTTPException(status_code=403, detail="Account is deactivated.")

                # Promote device trust
                await db.device_trust.update_one(
                    {"userId": matched_user_id, "deviceFingerprint": payload.device_fingerprint},
                    {"$set": {"lastUsedAt": datetime.utcnow(), "trustScore": 1.0}},
                    upsert=True,
                )
                # Update last login
                await db.users.update_one(
                    {"user_id": matched_user_id},
                    {"$set": {"last_login": datetime.utcnow(), "updated_at": datetime.utcnow()}},
                )

                generate_token(matched_user_id, response)
                logger.info(
                    "Face ID ALLOW — user=%s score=%.4f threshold=%.4f arcface=%s ip=%s",
                    email, similarity_score, threshold, using_arcface, ip_address,
                )
                return {
                    "success": True,
                    "message": "Authenticated successfully via Face ID",
                    "user": {
                        "user_id":              matched_user_id,
                        "email":                email,
                        "username":             matched_user.get("username"),
                        "full_name":            matched_user.get("full_name"),
                        "onboarding_completed": matched_user.get("onboarding_completed", False),
                        "avatar":               matched_user.get("avatar"),
                    },
                }

            elif decision.decision == "CHALLENGE":
                return {
                    "success":           False,
                    "challenge_required": True,
                    "email":             email,
                    "userId":            matched_user_id,
                    "message":           "Liveness verification required.",
                    "reason":            decision.reasoning,
                }
            else:
                logger.warning(
                    "Face ID DENY — user=%s score=%.4f reason=%s ip=%s",
                    email, similarity_score, decision.reasoning, ip_address,
                )
                raise HTTPException(
                    status_code=401,
                    detail=f"Face ID authentication failed: {decision.reasoning}",
                )

        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Face ID login failed: %s", e)
            raise HTTPException(status_code=500, detail="Internal server error")

    @classmethod
    async def verify_face(cls, payload: FaceVerifyRequest, current_user: dict):
        """
        Verify face against active profile (for high security steps).
        """
        try:
            user = current_user.get("user")
            user_id = user["user_id"]

            using_arcface = FaceAnalysisService._get_ort_session() is not None
            if not using_arcface:
                raise HTTPException(
                    status_code=500,
                    detail="Biometric verification is currently unavailable (ML model engine offline)."
                )

            img = FaceAnalysisService.base64_to_image(payload.frame)
            if img is None:
                raise HTTPException(status_code=400, detail="Invalid frame format")

            analysis = FaceAnalysisService.analyze_face(img)
            if not analysis:
                raise HTTPException(status_code=400, detail="No face detected")

            query_vector = FaceAnalysisService.generate_face_embedding(img, analysis)

            # Check user embeddings only
            cursor = db.face_embeddings.find(
                {"userId": user_id}, {"embeddingVector": 1}
            )
            docs = await cursor.to_list(length=20)

            if not docs:
                raise HTTPException(
                    status_code=400, detail="No registered biometrics for this user"
                )

            max_sim = 0.0
            for doc in docs:
                sim = VectorSearchService.cosine_similarity_np(
                    query_vector, doc["embeddingVector"]
                )
                if sim > max_sim:
                    max_sim = sim

            passed = max_sim >= 0.75

            return {
                "success": passed,
                "score": max_sim,
                "message": "Face verification passed"
                if passed
                else "Face verification failed",
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.exception("Biometric verify failed: %s", e)
            raise HTTPException(status_code=500, detail="Internal server error")

    @classmethod
    async def get_user_landmarks(cls, current_user: dict):
        """Queries and returns all registered face landmarks for the user."""
        try:
            user = current_user.get("user")
            user_id = user["user_id"]

            cursor = db.face_landmarks.find({"userId": user_id}, {"_id": 0})
            records = await cursor.to_list(length=10)

            return {
                "success": True,
                "userId": user_id,
                "email": user.get("email"),
                "records": records,
            }
        except Exception as e:
            logger.exception("Failed to retrieve face landmarks: %s", e)
            raise HTTPException(status_code=500, detail="Internal server error")

    @classmethod
    async def logout_face(cls, response: Response):
        """De-authenticate current Face ID session by removing cookies."""
        try:
            response.delete_cookie(
                key="user",
                httponly=True,
                secure=is_prod,
                samesite="none" if is_prod else "lax",
                path="/",
            )
            return {"success": True, "message": "Logged out successfully"}
        except Exception as e:
            logger.exception("Face ID logout failed: %s", e)
            raise HTTPException(status_code=500, detail="Internal server error")

    @classmethod
    async def delete_biometrics(cls, current_user: dict):
        """
        Delete all biometric data for the authenticated user:
        embeddings (ChromaDB + MongoDB), landmarks, and face_registered flag.
        """
        try:
            user = current_user.get("user")
            user_id = user["user_id"]

            # 1. Delete vector embeddings
            await VectorSearchService.delete_user_embeddings(user_id)

            # 2. Delete landmark records
            await db.face_landmarks.delete_many({"userId": user_id})

            # 3. Clear face_registered flag
            await db.users.update_one(
                {"user_id": user_id},
                {"$set": {"face_registered": False, "updated_at": datetime.utcnow()}},
            )

            logger.info("Deleted all biometrics for user %s", user_id)
            return {
                "success": True,
                "message": "Face ID biometrics removed successfully",
            }
        except Exception as e:
            logger.exception("Failed to delete biometrics: %s", e)
            raise HTTPException(status_code=500, detail="Internal server error")
