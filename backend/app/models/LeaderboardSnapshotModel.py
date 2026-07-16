# Copyright 2026 Sharexpress Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
