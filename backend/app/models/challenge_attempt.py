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
