import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_VERSION: str = Field(..., description="Service version", example="1.0.0")

    # JWT config
    ALGORITHM: str = Field(..., description="JWT algorithm", example="RS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        ..., description="Access token expiration minutes", example=30
    )

    # RSA keys config
    KEYS_PATH: str = Field(..., description="Keys path", example="keys")

    # Database config
    DATABASE_URL: str = Field(
        ..., description="Database URL", example="sqlite:///./data/app.db"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


_private_key = None
_public_key = None
settings = Settings()


def load_private_key() -> rsa.RSAPrivateKey:
    key_path = f"{settings.KEYS_PATH}/private.pem"
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"Private key not found at {key_path}")

    with open(key_path, "rb") as file:
        return serialization.load_pem_private_key(file.read(), password=None)


def load_public_key() -> rsa.RSAPublicKey:
    key_path = f"{settings.KEYS_PATH}/public.pem"
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"Public key not found at {key_path}")

    with open(key_path, "rb") as file:
        return serialization.load_pem_public_key(file.read())


def get_private_key() -> rsa.RSAPrivateKey:
    global _private_key
    if _private_key is None:
        _private_key = load_private_key()
    return _private_key


def get_public_key() -> rsa.RSAPublicKey:
    global _public_key
    if _public_key is None:
        _public_key = load_public_key()
    return _public_key
