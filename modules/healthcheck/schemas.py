"""
Healthcheck module validation schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    """Health check response schema"""
    status: str = Field(..., description="Service status", example="healthy")
    timestamp: datetime = Field(..., description="Current timestamp")
    version: Optional[str] = Field(None, description="Service version", example="1.0.0")
    service: Optional[str] = Field(None, description="Service name", example="auth-playground")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-01T00:00:00",
                "version": "1.0.0",
                "service": "auth-playground"
            }
        }

