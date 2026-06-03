from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4, UUID


class UserModel(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=30)

    email: EmailStr

    id: UUID = Field(default_factory=uuid4)

    full_name: Optional[str] = None

    bio: Optional[str] = None

    avatar: Optional[str] = None

    github_url: Optional[str] = None

    linkedin_url: Optional[str] = None

    portfolio_url: Optional[str] = None

    role: str = "user"

    auth_provider: Optional[str] = None

    frontend_rating: int = 0

    backend_rating: int = 0

    fullstack_rating: int = 0

    devops_rating: int = 0

    overall_rating: int = 0

    solved_problems: List[str] = []
    badges: List[str] = []
    streak_count: int = 0
    is_verified: bool = False
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()


class OTPverify(BaseModel):
    transactionID: str
    OTP: str


# SEARCH BY EMAIL


class email(BaseModel):
    email: EmailStr


class CompleteOnboarding(BaseModel):
    username: str

    full_name: str | None = None


#     "user_id": str,

#     "email": str,
#     "username": str,
#     "full_name": str,

#     "avatar": str,

#     "bio": str,

#     "country": str,

#     "role": "user",

#     "auth_provider": "google",

#     "is_verified": True,
#     "is_active": True,

#     "onboarding_completed": True,

#     # =====================================
#     # ENGINEERING RATINGS
#     # =====================================

#     "overall_rating": 0,

#     "frontend_rating": 0,
#     "backend_rating": 0,
#     "fullstack_rating": 0,
#     "devops_rating": 0,
#     "system_design_rating": 0,
#     "database_rating": 0,
#     "api_rating": 0,

#     # =====================================
#     # GAMIFICATION
#     # =====================================

#     "xp": 0,

#     "streak_count": 0,

#     "badges": [],

#     "weekly_xp": 0,

#     "global_rank": 0,
#     "weekly_rank": 0,

#     # =====================================
#     # COUNTERS
#     # =====================================

#     "total_solved": 0,

#     "total_interviews": 0,

#     "total_system_designs": 0,

#     "success_rate": 0,

#     # =====================================
#     # TIMESTAMPS
#     # =====================================

#     "created_at": datetime,
#     "updated_at": datetime,
#     "last_active": datetime,
# }
