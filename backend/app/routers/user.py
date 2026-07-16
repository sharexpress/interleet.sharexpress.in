# Copyright 2026 Sharexpress Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    # Clean and serialize user details
    return {
        "success": True,
        "user": UserController._public_user(user["user"]),
    }


@router.post("/complete-onboarding")
async def complete_onboarding(
    payload: CompleteOnboarding,
    user=Depends(User_Middleware.me),
):
    return await UserController.complete_onboarding(payload, user)


@router.post("/admin/login")
async def admin_login(
    payload: dict,
    response: Response,
):
    return await UserController.admin_login(payload, response)
