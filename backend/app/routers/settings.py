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

"""
Settings Router — /api/settings/*
Production-ready user settings, billing, and XP management endpoints.
"""

from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from app.controllers.settings_controller import SettingsController
from app.middleware.user import Middleware as UserMiddleware

router = APIRouter(prefix="/api/settings", tags=["Settings"])


@router.get("")
async def get_settings(user_auth=Depends(UserMiddleware.me)):
    """Get all user settings (notifications, privacy, preferences)."""
    return await SettingsController.get_settings(user_auth["user"])


@router.put("")
async def update_settings(
    payload: dict = Body(...),
    user_auth=Depends(UserMiddleware.me),
):
    """Update user settings. Accepts partial updates per section."""
    return await SettingsController.update_settings(user_auth["user"], payload)


@router.get("/billing")
async def get_billing(user_auth=Depends(UserMiddleware.me)):
    """Get billing information and payment history."""
    return await SettingsController.get_billing_info(user_auth["user"])


@router.get("/xp-history")
async def get_xp_history(
    limit: int = Query(default=50, ge=1, le=200),
    user_auth=Depends(UserMiddleware.me),
):
    """Get XP transaction history — every XP earn/spend event with audit trail."""
    return await SettingsController.get_xp_history(user_auth["user"], limit=limit)


@router.get("/sessions")
async def get_sessions(user_auth=Depends(UserMiddleware.me)):
    """Get active login sessions/devices."""
    return await SettingsController.get_active_sessions(user_auth["user"])


from fastapi import Response

@router.delete("/account")
async def delete_account(response: Response, user_auth=Depends(UserMiddleware.me)):
    """Soft-delete user account. Anonymizes PII and deactivates."""
    result = await SettingsController.delete_account(user_auth["user"])
    
    from app.core.config import PROJECT_ENVIRONMENT
    is_prod = PROJECT_ENVIRONMENT == "PRODUCTION"
    response.delete_cookie(
        key="user",
        httponly=True,
        secure=is_prod,
        samesite="none" if is_prod else "lax",
        path="/",
    )
    response.delete_cookie(
        key="guest_session",
        httponly=True,
        secure=is_prod,
        samesite="none" if is_prod else "lax",
        path="/",
    )
    return result
