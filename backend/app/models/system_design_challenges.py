from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class SystemDesignChallengeModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    slug: str
    title: str
    prompt: str
    difficulty: str = "Medium"
    topics: list[str] = Field(default_factory=list)
    template_id: str | None = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
