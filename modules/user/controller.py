from sqlalchemy.orm import Session
from .schemas import UserCreate
from .models import User
from .db_models import User as UserModel
from fastapi import HTTPException
import bcrypt

class UserController:
    """Controller for user operations"""

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        try:
            existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
            if existing_user:
                print(f"User already exists: {existing_user}")
                raise HTTPException(status_code=400, detail="User already exists")
            
            hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
            new_user = UserModel(email=user_data.email, hashed_password=hashed_password)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return User.from_db_model(new_user)
        except Exception as e:
            # TODO: add more specific error messages
            raise HTTPException(status_code=500, detail=f"Internal server error: {e}")