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


class RegisterUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None


class LoginUser(BaseModel):
    email: EmailStr
    password: str


# SEARCH BY EMAIL


class email(BaseModel):
    email: EmailStr
