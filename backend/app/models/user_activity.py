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

from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, Dict, Any
from enum import Enum


class ActivityType(str, Enum):
    CHALLENGE_STARTED = "challenge_started"
    CHALLENGE_SOLVED = "challenge_solved"
    CHALLENGE_FAILED = "challenge_failed"

    INTERVIEW_STARTED = "interview_started"
    INTERVIEW_COMPLETED = "interview_completed"

    SYSTEM_DESIGN_STARTED = "system_design_started"
    SYSTEM_DESIGN_COMPLETED = "system_design_completed"

    BADGE_EARNED = "badge_earned"

    STREAK_MILESTONE = "streak_milestone"

    XP_EARNED = "xp_earned"

    RANK_UPDATED = "rank_updated"


class UserActivityModel(BaseModel):
    activity_id: UUID = Field(default_factory=uuid4)

    user_id: UUID

    type: ActivityType

    title: str

    description: Optional[str] = None

    domain: Optional[str] = None

    reference_id: Optional[UUID] = None

    xp_earned: int = 0

    metadata: Dict[str, Any] = {}

    created_at: datetime = Field(default_factory=datetime.utcnow)
