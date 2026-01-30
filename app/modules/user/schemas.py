from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Create user request schema"""

    email: EmailStr
    password: str = Field(..., min_length=12)


class UserSignIn(BaseModel):
    """Sign in user request schema"""

    email: EmailStr
    password: str = Field(..., min_length=12)


class UserResponse(BaseModel):
    """User response schema"""

    id: str
    email: EmailStr
    email_verified: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserSignInResponse(BaseModel):
    """User sign in response schema"""

    user: UserResponse
    access_token: str
