from __future__ import annotations

from sqlalchemy.orm import Session

from app.modules.core import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    settings,
    verify_password,
)
from app.utils import ResponseSchema

from .db_models import User as UserModel
from .schemas import UserCreate, UserResponse, UserSignIn, UserSignInResponse


class UserController:
    """Controller for user operations"""

    @staticmethod
    def _generate_refresh_token(user: UserModel, db: Session) -> str:
        """Generate a refresh token for a user"""
        refresh_token = create_refresh_token()
        user.refresh_token = refresh_token
        db.commit()
        return refresh_token

    @staticmethod
    def create_user(
        db: Session, user_data: UserCreate
    ) -> ResponseSchema[UserResponse] | ResponseSchema[None]:
        """Create a new user"""
        try:
            existing_user = (
                db.query(UserModel).filter(UserModel.email == user_data.email).first()
            )
            if existing_user:
                print(f"User already exists: {existing_user}")
                return ResponseSchema[None](
                    status=400,
                    message="User already exists",
                    error="User already exists",
                )

            hashed_password = get_password_hash(user_data.password)
            new_user = UserModel(email=user_data.email, hashed_password=hashed_password)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user_response = UserResponse.model_validate(new_user)
            return ResponseSchema[UserResponse](
                status=201, message="User created successfully", docs=[user_response]
            )
        except Exception as e:
            return ResponseSchema[None](
                status=500, message="Error creating user", error=str(e)
            )

    @staticmethod
    def sign_in(
        db: Session, user_data: UserSignIn
    ) -> tuple[ResponseSchema[None] | ResponseSchema[UserSignInResponse], str]:
        try:
            existing_user = (
                db.query(UserModel).filter(UserModel.email == user_data.email).first()
            )
            print("existing_user", existing_user)
            if not existing_user:
                return (
                    ResponseSchema[None](
                        status=400, message="User not found", error="User not found"
                    ),
                    "",
                )
            if not verify_password(user_data.password, existing_user.hashed_password):
                return (
                    ResponseSchema[None](
                        status=400, message="Invalid password", error="Invalid password"
                    ),
                    "",
                )
            validated_existing_user = UserResponse.model_validate(existing_user)
            # Create refresh token, save to DB, and set as HttpOnly cookie
            refresh_token = UserController._generate_refresh_token(existing_user, db)
            user_response = UserSignInResponse.model_validate(
                {
                    "user": validated_existing_user,
                    "access_token": create_access_token(
                        {
                            "id": validated_existing_user.id,
                            "email": validated_existing_user.email,
                            "email_verified": validated_existing_user.email_verified,
                        },
                        algorithm=settings.ALGORITHM,
                    ),
                }
            )
            return (
                ResponseSchema[UserSignInResponse](
                    status=200, message="Signed in successfully", docs=[user_response]
                ),
                refresh_token,
            )
        except Exception as e:
            return (
                ResponseSchema[None](
                    status=500, message="Error signing in", error=str(e)
                ),
                "",
            )
