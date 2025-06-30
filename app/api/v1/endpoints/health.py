"""
Health check endpoints for API monitoring

This module provides comprehensive health check endpoints that verify
the status of the API service, database connectivity, and system information.
"""

from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api.deps import get_db, check_database_connection
from app.core.config import settings
from app.schemas.base import MessageResponse

router = APIRouter()


@router.get("/", response_model=Dict[str, Any])
async def health_check(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Comprehensive health check endpoint
    
    Verifies the API service status, database connectivity, and provides
    system information. This is the main health check endpoint for monitoring.
    
    Returns:
        Dict containing:
        - status: Overall service status
        - service: Service name
        - environment: Current environment
        - database: Database connection status
        - timestamp: Current timestamp
        - version: API version
    """
    
    # Check database connection
    database_status = "connected"
    try:
        # Test database with a simple query
        db.execute(text("SELECT 1"))
        db.commit()
    except Exception as e:
        database_status = f"disconnected: {str(e)}"
    
    # Determine overall status
    overall_status = "healthy" if database_status == "connected" else "unhealthy"
    
    return {
        "status": overall_status,
        "service": settings.project_name,
        "environment": settings.environment,
        "database": database_status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0",
        "api_docs": "/docs"
    }


@router.get("/simple", response_model=Dict[str, Any])
async def simple_health_check() -> Dict[str, Any]:
    """
    Simple health check endpoint
    
    Returns a basic status message without database connectivity check.
    Useful for basic uptime monitoring.
    
    Returns:
        Dict: Simple success message
    """
    return {
        "message": f"{settings.project_name} is running",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/database", response_model=Dict[str, Any])
async def database_health_check(
    is_connected: bool = Depends(check_database_connection),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Database-specific health check endpoint
    
    Provides detailed information about database connectivity and status.
    
    Args:
        is_connected: Database connection status from dependency
        db: Database session
        
    Returns:
        Dict containing detailed database status information
    """
    
    try:
        # Get some database statistics
        result = db.execute(text("SELECT version()")).fetchone()
        db_version = result[0] if result else "Unknown"
        
        # Test a simple transaction
        db.execute(text("SELECT COUNT(*) FROM information_schema.tables"))
        
        return {
            "database": "connected",
            "status": "healthy",
            "version": db_version,
            "connection_pool": "active",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "database": "disconnected",
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        ) 