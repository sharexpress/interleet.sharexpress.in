from datetime import datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


ExecutionStatus = Literal["queued", "running", "completed", "failed", "timeout", "configuration_error"]


class ExecutionRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    problem_id: str | None = None
    problem_slug: str | None = None
    mode: Literal["run", "submit"] = "run"
    language: Literal["python", "javascript", "typescript", "java", "cpp", "go"] = "python"
    source_code: str = Field(alias="code")


class ExecutionJobModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str | None = None
    problem_slug: str | None = None
    problem_id: str | None = None
    mode: Literal["run", "submit"] = "run"
    language: str
    source_code: str
    status: ExecutionStatus = "queued"
    judge0_tokens: list[str] = Field(default_factory=list)
    testcase_ids: list[str] = Field(default_factory=list)
    results: list[dict[str, Any]] = Field(default_factory=list)
    passed: int = 0
    total: int = 0
    score: float = 0
    verdict: str = "Queued"
    runtime_ms: float | None = None
    memory_kb: int | None = None
    error: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None
