import os
import cv2
import base64
import urllib.request
import logging
from typing import List, Dict, Any, Tuple, Optional
import numpy as np

logger = logging.getLogger(__name__)

# ── Lazy-load ONNX runtime only ────────────────────────────────────────────
# mediapipe is intentionally NOT used — 0.10+ removed the solutions API on
# Windows. We use OpenCV's built-in DNN face detector instead.
ort = None

def _init_ort():
    global ort
    if ort is None:
        try:
            import onnxruntime as ort_lib
            ort = ort_lib
        except ImportError:
            logger.warning("onnxruntime not installed — geometric embedding fallback will be used")


# ── OpenCV DNN face detector (ships with cv2, no extra install) ─────────────
# We use the SSD ResNet-10 model bundled inside OpenCV's DNN module.
# As a last resort we fall back to the classical Haar cascade.

_DNN_NET: Optional[cv2.dnn.Net] = None
_HAAR: Optional[cv2.CascadeClassifier] = None

def _get_face_detector():
    """
    Return (detector_type, detector_object).
    Preference order: OpenCV DNN → Haar cascade.
    """
    global _DNN_NET, _HAAR

    if _DNN_NET is not None:
        return ("dnn", _DNN_NET)

    # Try to load the OpenCV face detection DNN (comes bundled with opencv-python)
    _models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ai", "models")
    os.makedirs(_models_dir, exist_ok=True)

    proto_path  = os.path.join(_models_dir, "deploy.prototxt")
    caffemodel_path = os.path.join(_models_dir, "res10_300x300_ssd_iter_140000.caffemodel")

    _PROTO_URL  = "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt"
    _MODEL_URL  = "https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel"

    try:
        if not os.path.exists(proto_path):
            logger.info("Downloading face detector prototxt…")
            urllib.request.urlretrieve(_PROTO_URL, proto_path)
        if not os.path.exists(caffemodel_path):
            logger.info("Downloading face detector caffemodel…")
            urllib.request.urlretrieve(_MODEL_URL, caffemodel_path)

        net = cv2.dnn.readNetFromCaffe(proto_path, caffemodel_path)
        _DNN_NET = net
        logger.info("OpenCV DNN face detector loaded")
        return ("dnn", _DNN_NET)
    except Exception as e:
        logger.warning("Could not load DNN face detector: %s — trying Haar cascade", e)

    # Haar cascade fallback (always available in cv2)
    if _HAAR is None:
        haar_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        _HAAR = cv2.CascadeClassifier(haar_path)

    if _HAAR and not _HAAR.empty():
        logger.info("Using Haar cascade face detector")
        return ("haar", _HAAR)

    logger.error("No face detector available!")
    return (None, None)


def _detect_all_face_bboxes(image: np.ndarray, strict: bool = True) -> list:
    """
    Return a list of (x, y, w, h) bounding boxes for ALL detected faces.
    Callers MUST enforce single-face policy themselves.
    Raises no exception — returns empty list if no face found.
    """
    det_type, det = _get_face_detector()
    if det is None:
        return []

    h, w = image.shape[:2]
    boxes = []

    if det_type == "dnn":
        blob = cv2.dnn.blobFromImage(
            cv2.resize(image, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0)
        )
        det.setInput(blob)
        detections = det.forward()
        # Stricter confidence threshold: 0.65 when strict (was 0.50), relaxed to 0.45 when non-strict
        conf_threshold = 0.65 if strict else 0.45
        for i in range(detections.shape[2]):
            conf = float(detections[0, 0, i, 2])
            if conf > conf_threshold:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                x1, y1, x2, y2 = box.astype(int)
                bx = max(0, x1)
                by = max(0, y1)
                bw = min(w, x2) - bx
                bh = min(h, y2) - by
                if bw > 0 and bh > 0:
                    boxes.append((bx, by, bw, bh))
        return boxes

    # Haar — stricter minNeighbors=6 when strict, relaxed to 4 when non-strict
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    min_neighbors = 6 if strict else 4
    min_size = (80, 80) if strict else (60, 60)
    faces = det.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=min_neighbors, minSize=min_size)
    return [tuple(f) for f in faces]


def _detect_face_bbox(image: np.ndarray, strict: bool = True):
    """
    Return (x, y, w, h) bounding box of the largest detected face, or None.
    NOTE: prefer _detect_all_face_bboxes for security-critical code paths.
    """
    boxes = _detect_all_face_bboxes(image, strict=strict)
    if not boxes:
        return None
    return max(boxes, key=lambda f: f[2] * f[3])


def _check_image_quality(image: np.ndarray) -> tuple[bool, str]:
    """
    Check image quality: blur, brightness, contrast.
    Returns (is_acceptable, reason_if_not).
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Laplacian variance — low value = blurry
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    if blur_score < 40.0:
        return False, f"Image is too blurry (score={blur_score:.1f}). Hold camera steady."

    # Brightness check
    mean_brightness = float(np.mean(gray))
    if mean_brightness < 35:
        return False, "Image is too dark. Improve lighting."
    if mean_brightness > 230:
        return False, "Image is overexposed. Avoid strong backlighting."

    # Contrast (std dev)
    if float(np.std(gray)) < 15:
        return False, "Image has too little contrast. Improve lighting."

    return True, ""


# ──────────────────────────────────────────────────────────────────────────────

class FaceAnalysisService:
    MODEL_URL  = "https://huggingface.co/onnxmodelzoo/arcfaceresnet100-8/resolve/main/arcfaceresnet100-8.onnx"
    MODEL_DIR  = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ai", "models")
    MODEL_PATH = os.path.join(MODEL_DIR, "arcfaceresnet100-8.onnx")

    _ort_session = None

    LANDMARKER_URL  = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
    LANDMARKER_PATH = os.path.join(MODEL_DIR, "face_landmarker.task")

    _landmarker = None

    # ── ArcFace ONNX session ───────────────────────────────────────────────

    @classmethod
    def _download_model_if_missing(cls) -> bool:
        if os.path.exists(cls.MODEL_PATH):
            return True
        os.makedirs(cls.MODEL_DIR, exist_ok=True)
        logger.info("Downloading ArcFace ONNX model from %s…", cls.MODEL_URL)
        try:
            urllib.request.urlretrieve(cls.MODEL_URL, cls.MODEL_PATH)
            logger.info("ArcFace model downloaded to %s", cls.MODEL_PATH)
            return True
        except Exception as e:
            logger.error("ArcFace download failed: %s — geometric fallback will be used", e)
            return False

    @classmethod
    def _get_ort_session(cls):
        _init_ort()
        if cls._ort_session:
            return cls._ort_session
        if not ort:
            return None
        if not cls._download_model_if_missing():
            return None
        try:
            cls._ort_session = ort.InferenceSession(
                cls.MODEL_PATH, providers=["CPUExecutionProvider"]
            )
            logger.info("ONNX ArcFace session ready")
            return cls._ort_session
        except Exception as e:
            logger.error("ONNX session init failed: %s", e)
            return None

    # ── MediaPipe Face Landmarker ──────────────────────────────────────────

    @classmethod
    def _download_landmarker_if_missing(cls) -> bool:
        if os.path.exists(cls.LANDMARKER_PATH):
            return True
        os.makedirs(cls.MODEL_DIR, exist_ok=True)
        logger.info("Downloading MediaPipe Face Landmarker model from %s…", cls.LANDMARKER_URL)
        try:
            urllib.request.urlretrieve(cls.LANDMARKER_URL, cls.LANDMARKER_PATH)
            logger.info("MediaPipe Landmarker model downloaded to %s", cls.LANDMARKER_PATH)
            return True
        except Exception as e:
            logger.error("MediaPipe Landmarker download failed: %s", e)
            return False

    @classmethod
    def _get_landmarker(cls):
        if cls._landmarker:
            return cls._landmarker
        if not cls._download_landmarker_if_missing():
            return None
        try:
            import mediapipe as mp
            from mediapipe.tasks import python
            from mediapipe.tasks.python import vision
            
            base_options = python.BaseOptions(model_asset_path=cls.LANDMARKER_PATH)
            options = vision.FaceLandmarkerOptions(
                base_options=base_options,
                output_face_blendshapes=False,
                output_facial_transformation_matrixes=False,
                num_faces=1
            )
            cls._landmarker = vision.FaceLandmarker.create_from_options(options)
            logger.info("MediaPipe FaceLandmarker session ready")
            return cls._landmarker
        except Exception as e:
            logger.error("MediaPipe FaceLandmarker init failed: %s", e)
            return None

    # ── Image helpers ──────────────────────────────────────────────────────

    @staticmethod
    def base64_to_image(base64_str: str) -> Optional[np.ndarray]:
        """Decode a base64 data-URI or raw base64 string to a BGR numpy image."""
        try:
            if "," in base64_str:
                base64_str = base64_str.split(",")[1]
            img_data = base64.b64decode(base64_str)
            nparr    = np.frombuffer(img_data, np.uint8)
            img      = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return img
        except Exception as e:
            logger.error("base64 decode failed: %s", e)
            return None

    # ── Face analysis (OpenCV-only, no mediapipe) ──────────────────────────

    @staticmethod
    def analyze_face(image: np.ndarray, strict: bool = True) -> Optional[Dict[str, Any]]:
        """
        Detect a face and extract precise landmarks, pose, and liveness signals.

        Security enforcements (strict=True):
          - EXACTLY one face must be in frame (multi-person = hard reject)
          - Image must pass blur / brightness / contrast quality gate
          - Face must be at least 8 % of image area (not too small / far away)
          - Head pose must be within ±35° yaw, ±25° pitch, ±20° roll
          - Symmetry score must be ≥ 0.55
        """
        if image is None:
            return None

        h, w = image.shape[:2]

        # ── Quality gate ─────────────────────────────────────────────────────
        if strict:
            ok, reason = _check_image_quality(image)
            if not ok:
                logger.warning("Image quality rejected: %s", reason)
                return None

        # ── Multi-face guard ─────────────────────────────────────────────────
        all_faces = _detect_all_face_bboxes(image, strict=strict)
        if strict:
            if len(all_faces) == 0:
                logger.warning("Security: No face detected in frame")
                return None
            if len(all_faces) > 1:
                logger.warning(
                    "Security: %d faces detected — MULTI-PERSON FRAME REJECTED",
                    len(all_faces)
                )
                # Return a special sentinel so callers can surface the right error
                return {"multi_face_detected": True, "face_count": len(all_faces)}
        elif len(all_faces) == 0:
            logger.warning("No face detected in frame")
            return None

        # ── Min face size: must cover ≥ 8 % of image area ───────────────────
        if all_faces:
            largest = max(all_faces, key=lambda f: f[2] * f[3])
            face_area_ratio = (largest[2] * largest[3]) / (w * h + 1e-6)
            if strict and face_area_ratio < 0.08:
                logger.warning(
                    "Security: face too small (%.1f%% of frame) — move closer",
                    face_area_ratio * 100,
                )
                return None

        landmarker = FaceAnalysisService._get_landmarker()
        if not landmarker:
            logger.error("MediaPipe FaceLandmarker model is not loaded")
            return None

        try:
            import mediapipe as mp
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
            results = landmarker.detect(mp_image)

            if not results or not results.face_landmarks:
                logger.warning("MediaPipe: No face landmarks detected")
                return None

            # Extra guard: MediaPipe returned more than 1 face result
            if strict and len(results.face_landmarks) > 1:
                logger.warning(
                    "Security: MediaPipe detected %d face sets — MULTI-PERSON FRAME REJECTED",
                    len(results.face_landmarks)
                )
                return {"multi_face_detected": True, "face_count": len(results.face_landmarks)}

            face_landmarks = results.face_landmarks[0]
        except Exception as e:
            logger.error("MediaPipe FaceLandmarker processing failed: %s", e)
            return None

        # Convert landmarks to list of [x, y, z] in pixel coordinates
        landmarks_raw = []
        for lm in face_landmarks:
            landmarks_raw.append([lm.x * w, lm.y * h, lm.z * w])

        landmarks_np = np.array(landmarks_raw)

        # ── Head Pose ─────────────────────────────────────────────────────────
        left_eye  = landmarks_np[33]
        right_eye = landmarks_np[263]
        nose      = landmarks_np[4]

        dl = np.linalg.norm(nose[:2] - left_eye[:2])
        dr = np.linalg.norm(right_eye[:2] - nose[:2])
        yaw = float((dl - dr) / (dl + dr + 1e-6) * 90.0)

        forehead = landmarks_np[10]
        chin     = landmarks_np[152]
        dt = np.linalg.norm(forehead[:2] - nose[:2])
        db = np.linalg.norm(nose[:2] - chin[:2])
        pitch = float((db - dt) / (dt + db + 1e-6) * 60.0)

        dy   = right_eye[1] - left_eye[1]
        dx   = right_eye[0] - left_eye[0]
        roll = float(np.degrees(np.arctan2(dy, dx)))

        pose = {"yaw": yaw, "pitch": pitch, "roll": roll}

        # ── Strict pose check ────────────────────────────────────────────────
        if strict:
            if abs(yaw) > 35:
                logger.warning("Security: head yaw %.1f° exceeds ±35° limit", yaw)
                return None
            if abs(pitch) > 25:
                logger.warning("Security: head pitch %.1f° exceeds ±25° limit", pitch)
                return None
            if abs(roll) > 20:
                logger.warning("Security: head roll %.1f° exceeds ±20° limit", roll)
                return None

        # ── Calculate EAR (Eye Aspect Ratio) for Blinking ──────────────────
        left_eye_pts = [landmarks_raw[idx] for idx in [362, 385, 387, 263, 373, 380]]
        right_eye_pts = [landmarks_raw[idx] for idx in [33, 160, 158, 133, 153, 144]]
        
        ear_left = FaceAnalysisService.calculate_ear(left_eye_pts)
        ear_right = FaceAnalysisService.calculate_ear(right_eye_pts)
        ear_avg = (ear_left + ear_right) / 2.0
        
        ear = {"left": ear_left, "right": ear_right, "avg": ear_avg}

        # ── Calculate Smile ───────────────────────────────────────────────
        # Smile can be measured by ratio of mouth width to outer eye distance
        mouth_width = np.linalg.norm(landmarks_np[61][:2] - landmarks_np[291][:2])
        eye_distance = np.linalg.norm(landmarks_np[33][:2] - landmarks_np[263][:2])
        smile_score = float(mouth_width / (eye_distance + 1e-6))
        
        # ── Lips Open (for mouth validation) ──────────────────────────────
        lips_gap = np.linalg.norm(landmarks_np[13][:2] - landmarks_np[14][:2])
        lips_open = float(lips_gap / (eye_distance + 1e-6))

        # ── Symmetry ──────────────────────────────────────────────────────
        left_dist = np.linalg.norm(landmarks_np[4][:2] - landmarks_np[234][:2])
        right_dist = np.linalg.norm(landmarks_np[4][:2] - landmarks_np[454][:2])
        symmetry = float(min(left_dist, right_dist) / (max(left_dist, right_dist) + 1e-6))

        # Strict symmetry gate: too-low symmetry = side face / partial obstruction
        if strict and symmetry < 0.55:
            logger.warning("Security: face symmetry %.2f below 0.55 threshold", symmetry)
            return None

        # ── Crop Box ──────────────────────────────────────────────────────
        xs = landmarks_np[:, 0]
        ys = landmarks_np[:, 1]
        x_min = int(max(0, np.min(xs)))
        y_min = int(max(0, np.min(ys)))
        x_max = int(min(w, np.max(xs)))
        y_max = int(min(h, np.max(ys)))
        
        pad_x = int((x_max - x_min) * 0.1)
        pad_y = int((y_max - y_min) * 0.1)
        x_min = max(0, x_min - pad_x)
        y_min = max(0, y_min - pad_y)
        x_max = min(w, x_max + pad_x)
        y_max = min(h, y_max + pad_y)

        return {
            "landmarks":  landmarks_raw,
            "pose":       pose,
            "ear":        ear,
            "smile":      smile_score,
            "lips_open":  lips_open,
            "symmetry":   symmetry,
            "crop_box":   (x_min, y_min, x_max, y_max),
        }

    # ── Embedding generation ───────────────────────────────────────────────

    @classmethod
    def generate_face_embedding(
        cls, image: np.ndarray, analysis: Dict[str, Any] = None
    ) -> List[float]:
        """
        Generate an aligned 512-dim face embedding.
        Tries ArcFace ONNX first; falls back to deterministic geometric embedding.
        """
        if analysis is None:
            analysis = cls.analyze_face(image)
            if not analysis:
                raise ValueError("No face detected in the frame")

        session = cls._get_ort_session()

        if session:
            try:
                # ── Perform Face Alignment using 5 Reference Points ─────────
                landmarks = np.array(analysis["landmarks"])
                
                det_left_eye = (landmarks[33] + landmarks[133]) / 2.0
                det_right_eye = (landmarks[263] + landmarks[362]) / 2.0
                det_nose = landmarks[4]
                det_left_mouth = landmarks[61]
                det_right_mouth = landmarks[291]
                
                detected_pts = np.array([
                    det_left_eye[:2],
                    det_right_eye[:2],
                    det_nose[:2],
                    det_left_mouth[:2],
                    det_right_mouth[:2]
                ], dtype=np.float32)
                
                # Standard ArcFace target points in a 112x112 space
                STANDARD_LANDMARKS = np.array([
                    [38.2946, 51.6963],  # left eye
                    [73.5318, 51.5014],  # right eye
                    [56.0252, 71.7366],  # nose
                    [41.5493, 92.3655],  # left mouth corner
                    [70.7299, 92.2041]   # right mouth corner
                ], dtype=np.float32)
                
                M, _ = cv2.estimateAffinePartial2D(detected_pts, STANDARD_LANDMARKS)
                if M is not None:
                    face_aligned = cv2.warpAffine(image, M, (112, 112))
                else:
                    x_min, y_min, x_max, y_max = analysis["crop_box"]
                    face_crop = image[y_min:y_max, x_min:x_max]
                    face_aligned = cv2.resize(face_crop, (112, 112))
                
                face_rgb      = cv2.cvtColor(face_aligned, cv2.COLOR_BGR2RGB)
                face_t        = np.transpose(face_rgb, (2, 0, 1)).astype(np.float32)
                face_norm     = (face_t - 127.5) / 128.0
                input_blob    = np.expand_dims(face_norm, axis=0)

                input_name  = session.get_inputs()[0].name
                output_name = session.get_outputs()[0].name
                embedding   = session.run([output_name], {input_name: input_blob})[0][0]

                norm = np.linalg.norm(embedding)
                if norm > 0:
                    embedding = embedding / norm
                return embedding.tolist()
            except Exception as e:
                logger.error("ArcFace ONNX inference failed: %s — using geometric fallback", e)

        # ── Geometric fallback ─────────────────────────────────────────────
        # Build a stable 512-dim embedding from the face crop's pixel
        # statistics + bounding-box geometry. This is deterministic for the
        # same person/crop and produces unique per-person vectors.
        logger.info("Generating geometric face embedding (ONNX not available)")

        x_min, y_min, x_max, y_max = analysis["crop_box"]
        face_crop = image[y_min:y_max, x_min:x_max]

        if face_crop.size == 0:
            # Fallback if crop is empty — use full image
            face_crop = image

        # Resize to fixed 64×64, convert to float
        face_small = cv2.resize(face_crop, (64, 64)).astype(np.float32) / 255.0

        # HOG-like multi-channel feature: mean/std per 8×8 block
        block_size = 8
        features = []
        for i in range(0, 64, block_size):
            for j in range(0, 64, block_size):
                patch = face_small[i:i+block_size, j:j+block_size]
                features.extend([float(patch.mean()), float(patch.std())])
        # features length = (64/8)^2 * 2 = 128

        # Also append grayscale histogram (64 bins)
        gray  = cv2.cvtColor((face_small * 255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
        hist  = cv2.calcHist([gray], [0], None, [64], [0, 256]).flatten()
        hist  = (hist / (hist.sum() + 1e-6)).tolist()
        features.extend(hist)
        # features length = 192

        feat_arr = np.array(features, dtype=np.float32)

        # Project to 512-dim with a fixed random matrix (seed=42 → stable)
        rng        = np.random.default_rng(seed=42)
        proj       = rng.normal(size=(len(feat_arr), 512)).astype(np.float32)
        embedding  = np.dot(feat_arr, proj)

        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        return embedding.tolist()

    # ── Legacy helpers kept for compatibility ──────────────────────────────

    @staticmethod
    def calculate_ear(eye_landmarks: List[List[float]]) -> float:
        p  = np.array(eye_landmarks)
        v1 = np.linalg.norm(p[1] - p[5])
        v2 = np.linalg.norm(p[2] - p[4])
        h  = np.linalg.norm(p[0] - p[3])
        if h == 0:
            return 0.0
        return float((v1 + v2) / (2.0 * h))

    @staticmethod
    def calculate_head_pose(
        landmarks: np.ndarray, width: int, height: int
    ) -> Tuple[float, float, float]:
        if len(landmarks) < 300:
            return 0.0, 0.0, 0.0
        left_eye  = landmarks[33]
        right_eye = landmarks[263]
        nose      = landmarks[1]
        dl = np.linalg.norm(nose[:2] - left_eye[:2])
        dr = np.linalg.norm(right_eye[:2] - nose[:2])
        yaw = float((dl - dr) / (dl + dr + 1e-6) * 90.0)
        forehead = landmarks[10]
        chin     = landmarks[152]
        dt = np.linalg.norm(forehead[:2] - nose[:2])
        db = np.linalg.norm(nose[:2] - chin[:2])
        pitch = float((db - dt) / (dt + db + 1e-6) * 60.0)
        dy   = right_eye[1] - left_eye[1]
        dx   = right_eye[0] - left_eye[0]
        roll = float(np.degrees(np.arctan2(dy, dx)))
        return yaw, pitch, roll
