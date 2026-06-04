from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import List
from enum import Enum


class LeaderboardType(str, Enum):
    GLOBAL = "global"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

    FRONTEND = "frontend"
    BACKEND = "backend"
    FULLSTACK = "fullstack"
    DEVOPS = "devops"
    SYSTEM_DESIGN = "system_design"


class LeaderboardEntryModel(BaseModel):
    user_id: UUID

    username: str

    avatar: str | None = None

    rank: int

    rating: int

    xp: int

    badges_count: int = 0

    rank_change: int = 0


class LeaderboardSnapshotModel(BaseModel):
    snapshot_id: UUID = Field(default_factory=uuid4)

    leaderboard_type: LeaderboardType

    entries: List[LeaderboardEntryModel] = []

    generated_at: datetime = Field(default_factory=datetime.utcnow)

    created_at: datetime = Field(default_factory=datetime.utcnow)
