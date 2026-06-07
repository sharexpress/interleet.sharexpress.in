from fastapi import APIRouter, Depends, Response, Request
from app.models.passkey_models import (
    PasskeyRegisterOptionsRequest,
    PasskeyRegisterVerifyRequest,
    PasskeyLoginOptionsRequest,
    PasskeyLoginVerifyRequest
)
from app.controllers.passkey_controller import PasskeyController
from app.middleware.user import Middleware as User_Middleware

router = APIRouter(
    prefix="/api/passkey",
    tags=["Native Biometrics / Passkeys"],
)

@router.post("/register/options")
async def register_options(
    payload: PasskeyRegisterOptionsRequest,
    request: Request,
    current_user: dict = Depends(User_Middleware.me),
):
    """Get FIDO2 registration options. Requires user to be authenticated."""
    return await PasskeyController.register_options(payload, request, current_user)

@router.post("/register/verify")
async def register_verify(
    payload: PasskeyRegisterVerifyRequest,
    request: Request,
    current_user: dict = Depends(User_Middleware.me),
):
    """Verify and register FIDO2 public key credential. Requires user to be authenticated."""
    return await PasskeyController.register_verify(payload, request, current_user)

@router.post("/login/options")
async def login_options(
    payload: PasskeyLoginOptionsRequest,
    request: Request,
):
    """Get FIDO2 authentication options for login (1-1 matching)."""
    return await PasskeyController.login_options(payload, request)

@router.post("/login/verify")
async def login_verify(
    payload: PasskeyLoginVerifyRequest,
    request: Request,
    response: Response,
):
    """Verify signature and authenticate user using WebAuthn/Passkey."""
    return await PasskeyController.login_verify(payload, request, response)
