from pydantic import Field
from pydantic_settings import BaseSettings
from cryptography.hazmat.primitives.asymmetric import rsa

class Settings(BaseSettings):
    SERVICE_VERSION: str = Field(..., description="Service version", example="1.0.0")
    
    # JWT config
    ALGORITHM: str = Field(..., description="JWT algorithm", example="RS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., description="Access token expiration minutes", example=30)

    # RSA keys config
    KEYS_PATH: str = Field(..., description="Keys path", example="keys")

    # Database config
    DATABASE_URL: str = Field(..., description="Database URL", example="sqlite:///./data/app.db")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

_private_key = None
_public_key = None
settings = Settings()