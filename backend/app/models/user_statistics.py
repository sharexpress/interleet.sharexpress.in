from datetime import datetime
from pydantic import BaseModel, Field


class UserStatisticsModel(BaseModel):
    user_id: str
    xp: int = 0
    rating: int = 0
    rank: int | None = None
    streak: int = 0
    accuracy: int = 0
    solved: int = 0
    interviews: int = 0
    domain_scores: list[dict[str, int | str]] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
