from fastapi import APIRouter, Depends, Response, Request
from app.models.face_models import (
    FaceRegisterRequest,
    FaceLoginRequest,
    FaceVerifyRequest,
    LivenessChallengeVerifyRequest,
    LivenessChallengeStartRequest
)
from app.controllers.face_controller import FaceController
from app.middleware.user import Middleware as User_Middleware
from app.utils.JWT import check_token

router = APIRouter(
    prefix="/api/face",
    tags=["Face ID Biometrics"],
)


@router.post("/register")
async def register_face(
    payload: FaceRegisterRequest,
    response: Response,
    current_user: dict = Depends(User_Middleware.me),
):
    """Enroll a user's biometrics. Requires authentication (called from Settings)."""
    return await FaceController.register_face(payload, response, current_user)


@router.post("/login")
async def login_face(
    payload: FaceLoginRequest,
    response: Response,
    request: Request,
):
    """Authenticate and log in a user using face verification. No prior auth required."""
    return await FaceController.login_face(payload, response, request)


@router.post("/verify")
async def verify_face(
    payload: FaceVerifyRequest,
    current_user: dict = Depends(User_Middleware.me),
):
    """Perform mid-session verification for sensitive operations."""
    return await FaceController.verify_face(payload, current_user)


@router.post("/liveness/start")
async def start_liveness(
    payload: LivenessChallengeStartRequest
):
    """Request a random liveness verification command."""
    return await FaceController.get_active_challenge(payload)


@router.post("/liveness")
async def verify_liveness(
    payload: LivenessChallengeVerifyRequest
):
    """Verify sequence of frames against active liveness challenge."""
    return await FaceController.verify_liveness(payload)


@router.get("/session")
async def get_session(
    current_user: dict = Depends(User_Middleware.me),
):
    """Retrieve active biometrics state of the current session."""
    user = current_user.get("user", {})
    return {
        "success": True,
        "user_id": user.get("user_id"),
        "face_registered": user.get("face_registered", False),
        "last_login": user.get("last_login")
    }


@router.get("/landmarks")
async def get_landmarks(
    current_user: dict = Depends(User_Middleware.me),
):
    """Retrieve registered biometrics landmarks and angle crops."""
    return await FaceController.get_user_landmarks(current_user)


@router.delete("/biometrics")
async def delete_biometrics(
    current_user: dict = Depends(User_Middleware.me),
):
    """Delete all face biometric data for the authenticated user."""
    return await FaceController.delete_biometrics(current_user)


@router.post("/logout")
async def logout(
    response: Response,
    _: dict = Depends(User_Middleware.me),
):
    """De-authenticate current face session."""
    return await FaceController.logout_face(response)

