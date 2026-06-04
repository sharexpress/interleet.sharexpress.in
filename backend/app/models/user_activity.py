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
