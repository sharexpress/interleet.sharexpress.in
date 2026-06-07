"""
DeepFace-Compatible Service
============================
Acts as the face-comparison layer for Interleet's Face ID pipeline.

Python 3.14 Compatibility Note
-------------------------------
• deepface    requires TensorFlow  (no Python 3.14 wheels yet)
• face_recognition  requires dlib  (requires Visual C++ compiler on Windows)
• insightface requires onnxruntime (already installed ✓)

Strategy
---------
This service exposes the same API you'd expect from DeepFace but runs
entirely on what is already installed:

  1. Multi-face detection  → OpenCV DNN / Haar (from face_analysis._detect_all_face_bboxes)
  2. Embedding extraction → ArcFace ONNX session (from face_analysis.FaceAnalysisService)
  3. Face verification    → L2-normalised cosine similarity between ArcFace embeddings

When deepface IS eventually installable (Python 3.12 venv or future 3.14 wheel),
uncomment the DEEPFACE_AVAILABLE block to automatically use it as the primary engine.

API Surface (deepface-compatible):
  DeepFaceService.count_faces(image)               → int
  DeepFaceService.get_embedding(image)              → list[float]
  DeepFaceService.verify(img_login, img_enrolled)   → dict {verified, distance, threshold, model}
  DeepFaceService.verify_from_b64(b64, img)         → dict
"""

import logging
import base64
import cv2
import numpy as np
import os
from typing import Optional

logger = logging.getLogger(__name__)

# ── ArcFace cosine threshold ──────────────────────────────────────────────────
# Same-person ArcFace embeddings typically score > 0.85 cosine similarity.
# We accept login if cosine_similarity >= (1 - threshold), i.e. distance < threshold.
# Using 0.40 → cosine similarity must be ≥ 0.60 (conservative / secure)
VERIFY_THRESHOLD = float(os.getenv("FACE_VERIFY_THRESHOLD", "0.40"))


# ── Optional: DeepFace (Python 3.12 / TF available) ──────────────────────────
# To enable: install deepface + tf-keras in a Python 3.12 venv.
# Uncomment below and it will auto-activate at startup.
#
# DEEPFACE_AVAILABLE = False
# try:
#     from deepface import DeepFace as _DeepFace
#     DEEPFACE_AVAILABLE = True
#     logger.info("DeepFace (TF backend) activated")
# except ImportError:
#     pass


# ── Image decode helper ────────────────────────────────────────────────────────

def _b64_to_numpy(b64_str: str) -> Optional[np.ndarray]:
    try:
        if "," in b64_str:
            b64_str = b64_str.split(",")[1]
        data = base64.b64decode(b64_str)
        arr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        logger.error("base64 decode error: %s", e)
        return None


def _cosine_distance(v1: list, v2: list) -> float:
    a1 = np.array(v1, dtype=np.float32)
    a2 = np.array(v2, dtype=np.float32)
    n1 = np.linalg.norm(a1)
    n2 = np.linalg.norm(a2)
    if n1 == 0 or n2 == 0:
        return 1.0
    return float(1.0 - np.dot(a1, a2) / (n1 * n2))


# ── DeepFaceService ───────────────────────────────────────────────────────────

class DeepFaceService:
    """
    Face comparison service.
    Primary engine: ArcFace ONNX (already installed, Python 3.14 compatible).
    Drop-in for DeepFace when TF wheels become available.
    """

    # ── Face counting ──────────────────────────────────────────────────────────

    @staticmethod
    def count_faces(image: np.ndarray, strict: bool = True) -> int:
        """
        Count the number of distinct faces in a frame.
        Uses the existing multi-face detection pipeline (OpenCV DNN or Haar).
        Returns 0 on failure or empty frame.
        """
        try:
            from app.services.face_analysis import _detect_all_face_bboxes
            boxes = _detect_all_face_bboxes(image, strict=strict)
            count = len(boxes)
            logger.info("DeepFaceService.count_faces: %d face(s) detected (strict=%s)", count, strict)
            return count
        except Exception as e:
            logger.warning("DeepFaceService.count_faces error: %s", e)
            return 0

    # ── Embedding extraction ───────────────────────────────────────────────────

    @staticmethod
    def get_embedding(image: np.ndarray) -> Optional[list]:
        """
        Extract a 512-dim ArcFace embedding (L2-normalised).
        Returns None if no face found or ArcFace model unavailable.
        """
        try:
            from app.services.face_analysis import FaceAnalysisService
            # Use non-strict mode so we don't double-enforce all gates here
            analysis = FaceAnalysisService.analyze_face(image, strict=False)
            if not analysis or analysis.get("multi_face_detected"):
                logger.warning("DeepFaceService.get_embedding: no usable face in image")
                return None
            embedding = FaceAnalysisService.generate_face_embedding(image, analysis)
            if embedding:
                # L2-normalise
                arr = np.array(embedding, dtype=np.float32)
                norm = np.linalg.norm(arr)
                if norm > 0:
                    arr = arr / norm
                return arr.tolist()
            return None
        except Exception as e:
            logger.error("DeepFaceService.get_embedding error: %s", e)
            return None

    # ── Direct face verification ───────────────────────────────────────────────

    @staticmethod
    def verify(
        img_login: np.ndarray,
        img_enrolled: np.ndarray,
        threshold: float = VERIFY_THRESHOLD,
    ) -> dict:
        """
        Compare a live login frame against a stored enrolled face crop.

        Pipeline:
          1. Extract ArcFace embedding from login frame
          2. Extract ArcFace embedding from enrolled crop
          3. Compute cosine distance
          4. verified = (distance < threshold)

        Returns:
            {
                "verified"  : bool,
                "distance"  : float,   # cosine distance (lower = more similar)
                "threshold" : float,
                "model"     : str,
                "similarity": float,   # cosine similarity (higher = more similar)
            }
        """
        _fail = {
            "verified"  : False,
            "distance"  : 1.0,
            "threshold" : threshold,
            "model"     : "arcface_onnx",
            "similarity": 0.0,
        }

        emb_login    = DeepFaceService.get_embedding(img_login)
        emb_enrolled = DeepFaceService.get_embedding(img_enrolled)

        if emb_login is None:
            logger.warning("DeepFaceService.verify: could not extract embedding from login frame")
            return _fail
        if emb_enrolled is None:
            logger.warning("DeepFaceService.verify: could not extract embedding from enrolled crop")
            return _fail

        distance   = _cosine_distance(emb_login, emb_enrolled)
        similarity = 1.0 - distance
        verified   = distance < threshold

        logger.info(
            "DeepFaceService.verify: verified=%s distance=%.4f similarity=%.4f threshold=%.4f",
            verified, distance, similarity, threshold,
        )

        return {
            "verified"  : verified,
            "distance"  : distance,
            "threshold" : threshold,
            "model"     : "arcface_onnx_cosine",
            "similarity": similarity,
        }

    # ── Verify from base64 ─────────────────────────────────────────────────────

    @staticmethod
    def verify_from_b64(
        b64_login: str,
        img_enrolled: np.ndarray,
        threshold: float = VERIFY_THRESHOLD,
    ) -> dict:
        """Decode a base64 login frame, then call verify()."""
        img_login = _b64_to_numpy(b64_login)
        if img_login is None:
            return {
                "verified"  : False,
                "distance"  : 1.0,
                "threshold" : threshold,
                "model"     : "arcface_onnx_cosine",
                "similarity": 0.0,
            }
        return DeepFaceService.verify(img_login, img_enrolled, threshold)
