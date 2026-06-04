from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4
from enum import Enum


class DashboardActivityType(str, Enum):
    challenge_solved = "challenge_solved"
    interview_completed = "interview_completed"
    badge_earned = "badge_earned"
    streak_updated = "streak_updated"


class WeeklyActivityItem(BaseModel):
    day: str

    solved: int = 0

    minutes_practiced: int = 0


class DomainStrengthItem(BaseModel):
    domain: str

    score: int = 0


class RecentActivityItem(BaseModel):
    type: DashboardActivityType

    text: str

    domain: Optional[str] = None

    created_at: datetime


class InterviewTrendItem(BaseModel):
    week: str

    score: int


class RecommendedChallengeItem(BaseModel):
    challenge_id: str

    title: str

    domain: str

    difficulty: str

    xp_reward: int = 0

    estimated_time_minutes: int = 0

    success_rate: int = 0

    tags: List[str] = []


class DashboardProfile(BaseModel):
    full_name: Optional[str] = None

    username: Optional[str] = None

    avatar: Optional[str] = None

    email: str


class DashboardStats(BaseModel):
    total_xp: int = 0

    weekly_xp: int = 0

    streak_count: int = 0

    global_rank: int = 0

    frontend_rating: int = 0

    backend_rating: int = 0

    fullstack_rating: int = 0

    devops_rating: int = 0

    overall_rating: int = 0

    success_rate: int = 0

    total_solved: int = 0

    total_interviews: int = 0


class DashboardModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    user_id: str

    profile: DashboardProfile

    stats: DashboardStats

    weekly_activity: List[WeeklyActivityItem] = []

    domain_strengths: List[DomainStrengthItem] = []

    recent_activity: List[RecentActivityItem] = []

    interview_trend: List[InterviewTrendItem] = []

    recommended_challenges: List[RecommendedChallengeItem] = []

    badges: List[str] = []

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)
