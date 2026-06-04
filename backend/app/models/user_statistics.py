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
