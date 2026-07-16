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
from typing import Optional
from enum import Enum


class AttemptStatus(str, Enum):
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    SOLVED = "solved"
    FAILED = "failed"
    ABANDONED = "abandoned"


class ChallengeAttemptModel(BaseModel):
    attempt_id: UUID = Field(default_factory=uuid4)

    user_id: UUID

    challenge_id: UUID

    status: AttemptStatus = AttemptStatus.STARTED

    score: float = 0

    xp_earned: int = 0

    rating_change: int = 0

    time_taken_minutes: int = 0

    hints_used: int = 0

    test_cases_passed: int = 0

    total_test_cases: int = 0

    ai_feedback: Optional[str] = None

    code_language: Optional[str] = None

    code_submission: Optional[str] = None

    started_at: datetime = Field(default_factory=datetime.utcnow)

    completed_at: Optional[datetime] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)
