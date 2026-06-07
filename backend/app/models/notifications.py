from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4


class NotificationModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    title: str
    message: str
    type: str = "system"  # "invite" | "contest_started" | "achievement" | "system"
    link: Optional[str] = None
    read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
