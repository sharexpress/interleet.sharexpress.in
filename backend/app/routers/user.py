from fastapi import (
    APIRouter,
    Response,
    Request,
    Depends,
)
from app.models.users import UserModel as User, OTPverify, CompleteOnboarding
from typing import Dict

from app.controllers.user import (
    UserController,
)
from app.utils.JWT import (
    check_token,
)
from app.middleware.user import Middleware as User_Middleware
from typing import Dict

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/send-otp")
async def send_otp(
    user: User,
    _: None = Depends(check_token),
):
    return await UserController.send_otp(user)


@router.post("/verify-otp")
async def verify_otp(
    otp: OTPverify,
    response: Response,
    request: Request,
    _: None = Depends(check_token),
):
    return await UserController.verify_otp(otp, response, request)


@router.get("/google/login")
async def google_login(request: Request):
    return await UserController.google_login(request)


@router.get("/google/callback")
async def google_callback(request: Request):
    return await UserController.google_callback(request)


@router.get("/github/login")
async def github_login(request: Request):
    return await UserController.github_login(request)


@router.get("/github/callback")
async def github_callback(request: Request):
    return await UserController.github_callback(request)


@router.post("/logout")
async def logout(response: Response, _: None = Depends(User_Middleware.me)):
    return await UserController.logout(response)


@router.get("/me")
async def get_user(user: Dict = Depends(User_Middleware.me)):
    # Middleware returns { "success": True, "user": {...} }
    # Return that directly — flat, lowercase, one level deep.
    # Previous bug: return {"SUCCESS": True, "USER": user}
    # which nested the entire middleware dict under "USER",
    # so Redux saw payload.USER.user.user instead of payload.user
    return {
        "success": True,
        "user": user["user"],
    }


@router.post("/complete-onboarding")
async def complete_onboarding(
    payload: CompleteOnboarding,
    user=Depends(User_Middleware.me),
):
    return await UserController.complete_onboarding(payload, user)
