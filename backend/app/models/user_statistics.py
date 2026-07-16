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

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserStatisticsModel(BaseModel):
    total_xp: int = 0

    weekly_xp: int = 0

    monthly_xp: int = 0

    global_rank: int = 0

    weekly_rank: int = 0

    percentile: float = 0

    streak_count: int = 0

    longest_streak: int = 0

    total_challenges_attempted: int = 0

    total_challenges_solved: int = 0

    total_interviews_completed: int = 0

    total_system_design_completed: int = 0

    total_contests_participated: int = 0

    success_rate: float = 0

    average_problem_score: float = 0

    average_interview_score: float = 0

    frontend_rating: int = 0

    backend_rating: int = 0

    fullstack_rating: int = 0

    devops_rating: int = 0

    system_design_rating: int = 0

    database_rating: int = 0

    api_rating: int = 0

    overall_rating: int = 0

    total_badges_earned: int = 0

    contribution_count: int = 0

    last_active_at: Optional[datetime] = None
