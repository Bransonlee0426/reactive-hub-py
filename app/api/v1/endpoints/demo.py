"""
Demo endpoints for testing API functionality

This module provides demo endpoints to showcase API features like
pagination, data validation, and response formatting.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends

from app.api.deps import get_pagination_params
from app.schemas.base import PaginatedResponse, MessageResponse
from app.core.config import settings

router = APIRouter()


# Sample demo data
DEMO_ITEMS = [
    {"id": i, "name": f"Demo Item {i}", "description": f"This is test item number {i}", "active": True}
    for i in range(1, 51)  # Create 50 demo items
]


@router.get("/info", response_model=Dict[str, Any])
async def api_info() -> Dict[str, Any]:
    """
    API information endpoint
    
    Returns information about the API version, features, and endpoints.
    Useful for API discovery and feature verification.
    
    Returns:
        Dict containing API information and available features
    """
    return {
        "message": f"Welcome to {settings.project_name}",
        "version": "1.0.0",
        "environment": settings.environment,
        "features": [
            "Health Monitoring",
            "Database Integration", 
            "Soft Delete Support",
            "Pagination",
            "CORS Support",
            "Interactive Documentation"
        ],
        "endpoints": {
            "health": "/api/v1/health",
            "demo_items": "/api/v1/demo/items",
            "docs": "/docs",
            "redoc": "/redoc"
        },
        "documentation": {
            "swagger_ui": f"http://localhost:{settings.port}/docs",
            "redoc": f"http://localhost:{settings.port}/redoc"
        }
    }


@router.get("/items", response_model=PaginatedResponse[Dict[str, Any]])
async def get_demo_items(
    pagination: dict = Depends(get_pagination_params)
) -> PaginatedResponse[Dict[str, Any]]:
    """
    Demo paginated items endpoint
    
    Returns a paginated list of demo items to showcase pagination functionality.
    This endpoint demonstrates how pagination works with the PaginatedResponse schema.
    
    Args:
        pagination: Pagination parameters (page, size, skip, limit)
        
    Returns:
        PaginatedResponse containing demo items with pagination information
        
    Query Parameters:
        - page: Page number (default: 1, minimum: 1)
        - size: Items per page (default: 10, minimum: 1, maximum: 100)
        
    Example:
        GET /api/v1/demo/items?page=2&size=5
    """
    
    # Get pagination parameters
    skip = pagination["skip"]
    limit = pagination["limit"]
    page = pagination["page"] 
    size = pagination["size"]
    
    # Simulate database pagination
    total_items = len(DEMO_ITEMS)
    paginated_items = DEMO_ITEMS[skip:skip + limit]
    
    # Create paginated response
    return PaginatedResponse.create(
        items=paginated_items,
        total=total_items,
        page=page,
        size=size
    )


@router.get("/items/{item_id}", response_model=Dict[str, Any])
async def get_demo_item(item_id: int) -> Dict[str, Any]:
    """
    Get single demo item by ID
    
    Returns a specific demo item by its ID. Demonstrates path parameter handling.
    
    Args:
        item_id: The ID of the item to retrieve
        
    Returns:
        Dict containing the demo item data
        
    Raises:
        HTTPException: 404 if item not found
    """
    from fastapi import HTTPException
    
    # Find item by ID
    item = next((item for item in DEMO_ITEMS if item["id"] == item_id), None)
    
    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"Demo item with ID {item_id} not found"
        )
    
    return {
        **item,
        "retrieved_at": "2024-06-30T10:30:00Z",
        "endpoint": f"/api/v1/demo/items/{item_id}"
    }


@router.post("/echo", response_model=Dict[str, Any])
async def echo_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Echo endpoint for testing POST requests
    
    Returns the received data back to the client. Useful for testing
    request/response handling and data validation.
    
    Args:
        data: Any JSON data sent in the request body
        
    Returns:
        Dict containing the echoed data plus metadata
    """
    return {
        "message": "Data received successfully",
        "echoed_data": data,
        "received_at": "2024-06-30T10:30:00Z",
        "data_type": type(data).__name__
    }


@router.get("/status", response_model=MessageResponse)
async def demo_status() -> MessageResponse:
    """
    Demo status endpoint
    
    Returns a simple status message demonstrating the MessageResponse schema.
    
    Returns:
        MessageResponse: Simple status message
    """
    return MessageResponse(
        message="Demo endpoints are working correctly!",
        success=True
    ) 