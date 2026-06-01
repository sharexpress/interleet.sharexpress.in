from datetime import datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


SubmissionStatus = Literal["queued", "running", "accepted", "wrong_answer", "runtime_error", "time_limit_exceeded", "compile_error"]


class SubmissionModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str | None = None
    problem_slug: str
    language: str
    source_code: str
    status: SubmissionStatus = "queued"
    verdict: str = "Queued"
    score: float = 0
    passed: int = 0
    total: int = 0
    runtime_ms: float | None = None
    memory_kb: int | None = None
    results: list[dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None
