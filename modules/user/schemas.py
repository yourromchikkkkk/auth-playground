from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """Create user request schema"""
    email: EmailStr
    password: str = Field(..., min_length=12)

# TODO: think of general response schema for all routers
class UserResponse(BaseModel):
    """User response schema"""
    id: str
    email: EmailStr
    email_verified: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True