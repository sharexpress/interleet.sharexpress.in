from datetime import datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


Difficulty = Literal["Easy", "Medium", "Hard", "Expert"]
Domain = Literal["Frontend", "Backend", "DevOps", "APIs", "Databases", "System Design"]


class TestCaseModel(BaseModel):
    name: str
    input: dict[str, Any] = Field(default_factory=dict)
    expected: Any = None
    hidden: bool = False


class ProblemModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    problem_id: str = Field(default_factory=lambda: str(uuid4()))
    slug: str | None = None
    title: str
    domain: Domain
    difficulty: Difficulty = "Medium"
    minutes: int = 45
    xp: int = 100
    completion: int = 0
    tags: list[str] = Field(default_factory=list)
    summary: str
    description: str | None = None
    starter_code: dict[str, str] = Field(default_factory=dict)
    test_cases: list[TestCaseModel] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    hints: list[str] = Field(default_factory=list)
    is_active: bool = True
    created_by: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
