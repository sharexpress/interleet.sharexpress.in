from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List
from enum import Enum


class InterviewDifficulty(str, Enum):
    EASY = "easy"
    INTERMEDIATE = "intermediate"
    HARD = "hard"


class InterviewStatus(str, Enum):
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class InterviewDomain(str, Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    FULLSTACK = "fullstack"
    DEVOPS = "devops"
    SYSTEM_DESIGN = "system_design"
    APIS = "apis"


class InterviewSessionModel(BaseModel):
    session_id: UUID = Field(default_factory=uuid4)

    user_id: UUID

    role_title: str

    domain: InterviewDomain

    difficulty: InterviewDifficulty

    status: InterviewStatus = InterviewStatus.STARTED

    overall_score: float = 0

    technical_score: float = 0

    communication_score: float = 0

    problem_solving_score: float = 0

    system_design_score: float = 0

    confidence_score: float = 0

    clarity_score: float = 0

    ai_feedback: Optional[str] = None

    strengths: List[str] = []

    weaknesses: List[str] = []

    recommended_topics: List[str] = []

    duration_minutes: int = 0

    rating_change: int = 0

    xp_earned: int = 0

    total_questions: int = 0

    answered_questions: int = 0

    transcript: Optional[str] = None

    started_at: datetime = Field(default_factory=datetime.utcnow)

    completed_at: Optional[datetime] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)
