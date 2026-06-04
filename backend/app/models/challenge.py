from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum


class ChallengeDomain(str, Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    FULLSTACK = "fullstack"
    DEVOPS = "devops"
    DATABASES = "databases"
    APIS = "apis"
    SYSTEM_DESIGN = "system_design"


class ChallengeDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class ChallengeModel(BaseModel):
    challenge_id: UUID = Field(default_factory=uuid4)

    title: str = Field(
        ...,
        min_length=5,
        max_length=120,
    )

    slug: str

    short_description: str = Field(
        ...,
        max_length=300,
    )

    description: str

    domain: ChallengeDomain

    difficulty: ChallengeDifficulty

    tags: List[str] = []

    technologies: List[str] = []

    xp_reward: int = 0

    rating_reward: int = 0

    estimated_time_minutes: int = 0

    attempts_count: int = 0

    completion_count: int = 0

    likes_count: int = 0

    bookmarks_count: int = 0

    success_rate: float = 0

    average_score: float = 0

    average_completion_time: float = 0

    recommended_for_beginner: bool = False

    trending_score: float = 0

    popularity_score: float = 0

    concepts: List[str] = []

    learning_resources: List[str] = []

    hints: List[str] = []

    supports_ai_review: bool = False

    supports_code_execution: bool = False

    supports_system_design_canvas: bool = False

    is_published: bool = True

    is_featured: bool = False

    is_archived: bool = False

    created_by: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)
