from .db_models import User as UserModel

class User:
    def __init__(self, id: str, email: str, hashed_password: str, email_verified: bool = False):
        self.id = id
        self.email = email
        self.hashed_password = hashed_password
        self.email_verified = email_verified

    @classmethod
    def from_db_model(cls,db_user: UserModel) -> "User":
        """Create a User model from a database user model"""
        return cls(
            id=db_user.id,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            email_verified=db_user.email_verified
        )
    
    def is_email_verified(self) -> bool:
        """Check if the user's email is verified"""
        return self.email_verified

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, email_verified={self.email_verified})"
