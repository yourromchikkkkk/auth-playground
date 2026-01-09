"""
Healthcheck module router
"""
from fastapi import APIRouter
from modules.healthcheck.controller import HealthCheckController
from modules.healthcheck.schemas import HealthCheckResponse

healthcheck_router = APIRouter(prefix="/healthcheck")


@healthcheck_router.get(
    "",
    response_model=HealthCheckResponse,
    summary="Health Check",
    description="Check the health status of the service",
    tags=["healthcheck"]
)
async def healthcheck():
    """
    Health check endpoint
    
    Returns:
        HealthCheckResponse: The health status of the service
    """
    controller = HealthCheckController()
    health_status = controller.get_health_status()
    return controller.format_response(health_status)

