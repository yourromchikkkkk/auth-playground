"""
Healthcheck module models
"""
from datetime import datetime
from typing import Optional


class HealthStatus:
    """Health status model"""
    def __init__(
        self,
        status: str,
        timestamp: datetime,
        version: Optional[str] = None,
        service: Optional[str] = None
    ):
        self.status = status
        self.timestamp = timestamp
        self.version = version
        self.service = service

