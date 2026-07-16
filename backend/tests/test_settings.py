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
Tests for user settings, badges, and notification preferences CRUD
"""
import pytest
from datetime import datetime
from app.controllers.settings_controller import SettingsController
from app.services.badge_service import BadgeService
from app.services.notification_service import NotificationService

@pytest.mark.asyncio
async def test_default_settings():
    # Mock user object
    user = {"user_id": "test_user_123", "email": "test@interleet.dev"}
    
    # Fetch settings — should generate default settings document
    res = await SettingsController.get_settings(user)
    assert res["success"] is True
    assert "settings" in res
    assert res["settings"]["user_id"] == "test_user_123"
    assert res["settings"]["privacy"]["profile_visible"] is True
    assert res["settings"]["notifications"]["email_challenges"] is True

@pytest.mark.asyncio
async def test_update_settings():
    user = {"user_id": "test_user_123"}
    payload = {
        "privacy": {"profile_visible": False},
        "notifications": {"email_challenges": False}
    }
    
    res = await SettingsController.update_settings(user, payload)
    assert res["success"] is True
    
    # Fetch updated settings
    res2 = await SettingsController.get_settings(user)
    assert res2["settings"]["privacy"]["profile_visible"] is False
    assert res2["settings"]["notifications"]["email_challenges"] is False

@pytest.mark.asyncio
async def test_badge_criteria():
    # Test badge catalog checking
    user_id = "test_user_123"
    progress = await BadgeService.get_badge_progress(user_id)
    assert progress["total"] > 0
    assert "earned" in progress
    assert "locked" in progress
