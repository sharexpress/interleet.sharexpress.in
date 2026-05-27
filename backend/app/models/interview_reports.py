from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class InterviewReportModel(BaseModel):
    session_id: str
    user_id: str | None = None
    role: str | None = None
    interview_type: str | None = None
    report: dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)
