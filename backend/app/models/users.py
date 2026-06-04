from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import datetime
from uuid import UUID, uuid4


class BadgeModel(BaseModel):
    badge_id: str

    earned_at: datetime = Field(default_factory=datetime.utcnow)


class DomainStrengthModel(BaseModel):
    frontend: int = 0
    backend: int = 0
    fullstack: int = 0
    devops: int = 0
    system_design: int = 0
    databases: int = 0
    apis: int = 0


class UserModel(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)

    email: EmailStr

    username: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=30,
    )

    full_name: Optional[str] = None

    avatar: Optional[str] = None

    bio: Optional[str] = None

    country: Optional[str] = None

    website: Optional[str] = None

    github_username: Optional[str] = None

    linkedin_url: Optional[str] = None

    portfolio_url: Optional[str] = None

    auth_provider: Optional[str] = None

    google_sub: Optional[str] = None

    github_id: Optional[str] = None

    github_username_oauth: Optional[str] = None

    role: str = "user"

    is_verified: bool = False

    is_active: bool = True

    is_locked: bool = False

    onboarding_completed: bool = False

    overall_rating: int = 0

    frontend_rating: int = 0

    backend_rating: int = 0

    fullstack_rating: int = 0

    devops_rating: int = 0

    system_design_rating: int = 0

    database_rating: int = 0

    api_rating: int = 0

    total_xp: int = 0

    weekly_xp: int = 0

    monthly_xp: int = 0

    global_rank: int = 0

    weekly_rank: int = 0

    percentile: float = 0

    streak_count: int = 0

    longest_streak: int = 0

    last_active_at: Optional[datetime] = None

    total_challenges_solved: int = 0

    total_challenges_attempted: int = 0

    total_interviews_completed: int = 0

    total_system_design_completed: int = 0

    total_contests_participated: int = 0

    success_rate: float = 0

    average_interview_score: float = 0

    average_problem_score: float = 0

    domain_strengths: DomainStrengthModel = DomainStrengthModel()

    badges: List[BadgeModel] = []

    solved_problems: List[str] = []

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)

    last_login: Optional[datetime] = None


class OTPverify(BaseModel):
    transactionID: str
    OTP: str


class email(BaseModel):
    email: EmailStr


class CompleteOnboarding(BaseModel):
    username: str

    full_name: str | None = None
