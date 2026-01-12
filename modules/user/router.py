from fastapi import APIRouter, Depends
from .controller import UserController
from .schemas import UserCreate, UserResponse
from sqlalchemy.orm import Session
from database.base import get_db

user_router = APIRouter(prefix="/users")

@user_router.post(
    "/sign-up",
    response_model=UserResponse,
    summary="Sign up a new user",
    description="Sign up a new user",
    tags=["users"]
)
async def sign_up(user_data: UserCreate, db: Session = Depends(get_db)):
    """Sign up a new user"""
    return UserController.create_user(db, user_data)