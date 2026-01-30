import hashlib
import secrets

import jwt
from passlib.context import CryptContext

from .config import get_private_key, get_public_key

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Get a password hash"""
    return pwd_context.hash(password)


def create_access_token(
    payload: dict, private_key: str = get_private_key(), algorithm: str = "RS256"
) -> str:
    """Create an access token"""
    encoded = jwt.encode(payload, private_key, algorithm)
    return encoded


def verify_access_token(
    token: str, public_key: str = get_public_key(), algorithm: str = "RS256"
) -> dict:
    """Verify an access token"""
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def create_refresh_token() -> str:
    """Create a random hash string for refresh token"""
    random_bytes = secrets.token_bytes(32)  # Generate 32 random bytes
    hash_string = hashlib.sha256(random_bytes).hexdigest()  # Create SHA256 hash
    return hash_string
