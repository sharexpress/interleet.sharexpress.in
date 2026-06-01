from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class ExecutionResultModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    execution_job_id: str
    submission_id: str | None = None
    problem_slug: str
    testcase_id: str
    judge0_token: str
    status: str
    verdict: str
    passed: bool = False
    runtime_ms: float | None = None
    memory_kb: int | None = None
    stdout: str = ""
    stderr: str = ""
    compile_output: str = ""
    analytics: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
