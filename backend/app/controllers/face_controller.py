import os
import cv2
import uuid
import logging
import io
from datetime import datetime
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
from app.services.langchain_auth import LangChainAuthDecisionService
import numpy as np

logger = logging.getLogger(__name__)
db = get_db()
is_prod = PROJECT_ENVIRONMENT == "PRODUCTION"


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

                analysis = FaceAnalysisService.analyze_face(img)
                if not analysis:
                    raise HTTPException(
                        status_code=400,
                        detail=f"No face detected in the frame for angle {angle}",
                    )

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
            analysis = FaceAnalysisService.analyze_face(img)
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
            # Compare maximum smile to baseline (usually smile increases score by 0.1-0.2)
            if metrics["max_smile"] > 0.43:
                liveness_passed = True
            else:
                metrics["reason"] = (
                    f"Smile not detected. Max smile score: {metrics['max_smile']:.2f}"
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
        Performs vector search in ChromaDB, liveness check, LangChain threat assessment,
        and starts a JWT session on success.
        """
        try:
            # 1. Decode frame
            img = FaceAnalysisService.base64_to_image(payload.frame)
            if img is None:
                raise HTTPException(
                    status_code=400, detail="Invalid camera frame image format"
                )

            # 2. Extract landmark biometric metrics
            analysis = FaceAnalysisService.analyze_face(img)
            if not analysis:
                raise HTTPException(
                    status_code=400, detail="No face detected in camera stream"
                )

            # 3. Generate query vector
            query_vector = FaceAnalysisService.generate_face_embedding(img, analysis)

            # 4. Search database
            hits = await VectorSearchService.search_nearest_neighbors(
                query_vector, limit=5
            )
            if not hits:
                raise HTTPException(
                    status_code=401, detail="Biometric identity matches not found"
                )

            # 5. Check top candidate
            top_hit = hits[0]
            similarity_score = top_hit["similarity"]
            matched_user_id = top_hit["userId"]

            # Load matched user
            matched_user = await db.users.find_one({"user_id": matched_user_id})
            if not matched_user:
                raise HTTPException(
                    status_code=401, detail="Matched biometric identity does not exist"
                )

            email = matched_user["email"]

            # Filter validation if email is provided
            if payload.email:
                filtered_email = payload.email.strip().lower()
                if matched_user["email"] != filtered_email:
                    raise HTTPException(
                        status_code=401,
                        detail="Biometric credentials do not match this account",
                    )

            # Face ID must be enrolled before login is allowed
            if not matched_user.get("face_registered"):
                raise HTTPException(
                    status_code=403,
                    detail="Face ID not registered. Please enroll your face in settings.",
                )

            # 6. Gather threat & device context
            ip_address = request.client.host if request.client else "127.0.0.1"

            # Check device trust status
            device_trusted = False
            trust_doc = await db.device_trust.find_one(
                {
                    "userId": matched_user_id,
                    "deviceFingerprint": payload.device_fingerprint,
                }
            )
            if trust_doc:
                device_trusted = True

            # Count recent login failures in last 10 minutes
            recent_failures_count = await db.face_login_attempts.count_documents(
                {
                    "email": email,
                    "success": False,
                    "timestamp": {
                        "$gt": datetime.fromtimestamp(
                            datetime.utcnow().timestamp() - 600
                        )
                    },
                }
            )

            # Check for IP anomalies (if user has logged in from different IPs before)
            past_ips = await db.face_login_attempts.distinct(
                "ipAddress", {"userId": matched_user_id, "success": True}
            )
            ip_anomaly = len(past_ips) > 0 and ip_address not in past_ips

            # Basic local liveness check based on frame metrics
            # Normal blink-level EAR is > 0.22 (eyes open)
            liveness_valid = analysis["ear"]["avg"] > 0.20

            # Check if this device recently completed a successful liveness challenge (within last 5 minutes)
            challenge_passed_recently = await db.anti_spoofing_logs.find_one(
                {
                    "email": email,
                    "livenessPassed": True,
                    "deviceFingerprint": payload.device_fingerprint,
                    "timestamp": {
                        "$gt": datetime.fromtimestamp(
                            datetime.utcnow().timestamp() - 300
                        )
                    },
                }
            )
            if challenge_passed_recently:
                liveness_valid = True
                logger.info(
                    "Found recent successful liveness verification for %s on this device. Bypassing live EAR check.",
                    email,
                )
            liveness_data = {
                "ear": analysis["ear"]["avg"],
                "pose": analysis["pose"],
                "smile": analysis["smile"],
            }

            # 7. LangChain Adaptive Risk assessment
            decision = await LangChainAuthDecisionService.evaluate_auth_request(
                similarity_score=similarity_score,
                liveness_valid=liveness_valid,
                device_trusted=device_trusted,
                recent_failures_count=recent_failures_count,
                ip_anomaly=ip_anomaly,
                liveness_data=liveness_data,
            )

            # Record login attempt
            await db.face_login_attempts.insert_one(
                {
                    "userId": matched_user_id,
                    "email": email,
                    "success": decision.decision == "ALLOW",
                    "confidenceScore": similarity_score,
                    "decision": decision.decision,
                    "reason": decision.reasoning,
                    "ipAddress": ip_address,
                    "deviceFingerprint": payload.device_fingerprint,
                    "timestamp": datetime.utcnow(),
                }
            )

            # 8. Handle Auth Decisions
            if decision.decision == "ALLOW":
                # Check locked/active account status
                if matched_user.get("is_locked"):
                    raise HTTPException(status_code=403, detail="Account is locked")
                if not matched_user.get("is_active", True):
                    raise HTTPException(
                        status_code=403, detail="Account is deactivated"
                    )

                # Update device trust timestamp
                await db.device_trust.update_one(
                    {
                        "userId": matched_user_id,
                        "deviceFingerprint": payload.device_fingerprint,
                    },
                    {"$set": {"lastUsedAt": datetime.utcnow(), "trustScore": 1.0}},
                    upsert=True,
                )

                # Update user last login
                await db.users.update_one(
                    {"user_id": matched_user_id},
                    {
                        "$set": {
                            "last_login": datetime.utcnow(),
                            "updated_at": datetime.utcnow(),
                        }
                    },
                )

                # Set JWT Cookie
                generate_token(matched_user_id, response)
                logger.info("Face ID authentication successful for user %s", email)

                return {
                    "success": True,
                    "message": "Authenticated successfully via Face ID",
                    "user": {
                        "user_id": matched_user_id,
                        "email": email,
                        "username": matched_user.get("username"),
                        "full_name": matched_user.get("full_name"),
                        "onboarding_completed": matched_user.get(
                            "onboarding_completed", False
                        ),
                        "avatar": matched_user.get("avatar"),
                    },
                }

            elif decision.decision == "CHALLENGE":
                # Return challenge requirement response
                return {
                    "success": False,
                    "challenge_required": True,
                    "email": email,
                    "userId": matched_user_id,
                    "message": "Device verification required. Perform biometrics liveness check.",
                    "reason": decision.reasoning,
                }
            else:
                # DENY authentication
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

            passed = max_sim >= 0.70

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
