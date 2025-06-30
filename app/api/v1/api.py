"""
Main API router for version 1

This module aggregates all v1 API endpoints into a single router
that can be included in the main FastAPI application.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health, demo
from app.core.config import settings

# Create the main API router for version 1
api_router = APIRouter()

# Include health check endpoints
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health Check"],
    responses={
        200: {"description": "Healthy"},
        503: {"description": "Service Unavailable"}
    }
)

# Include demo endpoints
api_router.include_router(
    demo.router,
    prefix="/demo",
    tags=["Demo & Testing"],
    responses={
        200: {"description": "Success"},
        404: {"description": "Not Found"},
        422: {"description": "Validation Error"}
    }
)

# Root API v1 endpoint
@api_router.get("/", tags=["API Info"])
async def api_v1_info():
    """
    API v1 root endpoint
    
    Returns information about the API v1 and available endpoints.
    This serves as the entry point for API v1 discovery.
    
    Returns:
        Dict containing API v1 information and endpoint listings
    """
    return {
        "message": f"Welcome to {settings.project_name} API v1",
        "version": "1.0.0",
        "environment": settings.environment,
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        },
        "available_endpoints": {
            "health_check": f"{settings.api_v1_str}/health",
            "simple_health": f"{settings.api_v1_str}/health/simple", 
            "database_health": f"{settings.api_v1_str}/health/database",
            "api_info": f"{settings.api_v1_str}/demo/info",
            "demo_items": f"{settings.api_v1_str}/demo/items",
            "single_item": f"{settings.api_v1_str}/demo/items/{{item_id}}",
            "echo_test": f"{settings.api_v1_str}/demo/echo",
            "demo_status": f"{settings.api_v1_str}/demo/status"
        },
        "features": [
            "Comprehensive Health Monitoring",
            "Database Connectivity Checks",
            "Pagination Support",
            "Request/Response Validation",
            "Interactive API Documentation",
            "CORS Support for Frontend Integration"
        ]
    } 