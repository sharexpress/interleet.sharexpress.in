from datetime import datetime
from pydantic import BaseModel, Field


class LeaderboardEntryModel(BaseModel):
    user_id: str | None = None
    username: str
    rank: int
    rating: int
    xp: int
    country: str | None = None
    delta: int = 0
    badges: list[str] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
