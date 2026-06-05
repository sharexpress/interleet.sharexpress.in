from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum


class ChallengeDomain(str, Enum):
    FRONTEND = "Frontend"
    BACKEND = "Backend"
    FULLSTACK = "Fullstack"
    DEVOPS = "DevOps"
    DATABASES = "Databases"
    APIS = "APIs"
    SYSTEM_DESIGN = "System Design"


class ChallengeDifficulty(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    EXPERT = "Expert"


class TestCase(BaseModel):
    id: str
    name: str
    stdin: str = ""
    expected_output: str = ""
    hidden: bool = False
    weight: int = 1


class StarterCode(BaseModel):
    typescript: Optional[str] = ""
    javascript: Optional[str] = ""
    python: Optional[str] = ""
    go: Optional[str] = ""


class ChallengeModel(BaseModel):
    challenge_id: UUID = Field(default_factory=uuid4)

    title: str = Field(..., min_length=5, max_length=120)
    slug: str = Field(..., min_length=3, max_length=120)

    # Frontend sends "summary", model stores as short_description
    short_description: str = Field(..., max_length=300)
    description: str = Field(default="")

    domain: ChallengeDomain
    difficulty: ChallengeDifficulty

    tags: List[str] = []
    technologies: List[str] = []
    hints: List[str] = []
    concepts: List[str] = []

    starter_code: Optional[StarterCode] = None
    test_cases: List[TestCase] = []
    learning_resources: List[str] = []

    # Stats — set by system, not by user
    xp_reward: int = Field(default=0, ge=0)
    rating_reward: int = Field(default=0, ge=0)
    estimated_time_minutes: int = Field(default=0, ge=0)
    attempts_count: int = 0
    completion_count: int = 0
    likes_count: int = 0
    bookmarks_count: int = 0
    success_rate: float = 0.0
    average_score: float = 0.0
    average_completion_time: float = 0.0
    trending_score: float = 0.0
    popularity_score: float = 0.0

    recommended_for_beginner: bool = False
    supports_ai_review: bool = False
    supports_code_execution: bool = False
    supports_system_design_canvas: bool = False

    is_published: bool = True
    is_featured: bool = False
    is_archived: bool = False

    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("slug")
    def slug_format(cls, v: str) -> str:
        import re

        if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", v):
            raise ValueError(
                "Slug must be lowercase letters, numbers, and hyphens only (e.g. build-a-rate-limiter)"
            )
        return v
