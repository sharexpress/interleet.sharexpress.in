from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum


class RoleEnum(str, Enum):
    frontend = "frontend"
    backend = "backend"
    devops = "devops"
    hr = "hr"
    behavioural = "behavioural"


class InterviewTypeEnum(str, Enum):
    technical = "technical"
    behavioural = "behavioural"
    hr = "hr"


class DifficultyEnum(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class MockTestModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    role: RoleEnum
    interview_type: InterviewTypeEnum
    difficulty: DifficultyEnum
    jd: str
    additional_context: Optional[str] = None
    total_questions: int = 8
    easy_questions: int = 2
    medium_questions: int = 3
    hard_questions: int = 3
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
