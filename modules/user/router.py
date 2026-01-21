from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from database.base import get_db
from utils import ResponseSchema

from .controller import UserController
from .schemas import UserCreate, UserResponse, UserSignIn, UserSignInResponse

user_router = APIRouter(prefix="/users")


@user_router.post(
    "/sign-up",
    response_model=ResponseSchema[UserResponse],
    summary="Sign up a new user",
    description="Sign up a new user",
    tags=["users"],
)
async def sign_up(user_data: UserCreate, db: Session = Depends(get_db)):
    """Sign up a new user"""
    return UserController.create_user(db, user_data)


@user_router.post(
    "/sign-in",
    response_model=ResponseSchema[UserSignInResponse],
    summary="Sign in a user",
    description="Sign in a user",
    tags=["users"],
)
async def sign_in(user_data: UserSignIn, response: Response, db: Session = Depends(get_db)):
    """Sign in a user"""
    (result, refresh_token) = UserController.sign_in(db, user_data)

    if refresh_token:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 7,  # 7 days
        )

    return result
