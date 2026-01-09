"""
Healthcheck module controller
"""
from datetime import datetime
from modules.healthcheck.models import HealthStatus
from modules.healthcheck.schemas import HealthCheckResponse


class HealthCheckController:
    """Controller for health check operations"""
    
    @staticmethod
    def get_health_status() -> HealthStatus:
        """
        Get the current health status of the service
        
        Returns:
            HealthStatus: The health status model
        """
        return HealthStatus(
            status="healthy",
            timestamp=datetime.utcnow(),
            version="1.0.0",
            service="auth-playground"
        )
    
    @staticmethod
    def format_response(health_status: HealthStatus) -> HealthCheckResponse:
        """
        Format health status model to response schema
        
        Args:
            health_status: The health status model
            
        Returns:
            HealthCheckResponse: The formatted response schema
        """
        return HealthCheckResponse(
            status=health_status.status,
            timestamp=health_status.timestamp,
            version=health_status.version,
            service=health_status.service
        )

