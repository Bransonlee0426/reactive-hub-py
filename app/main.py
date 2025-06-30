"""
Reactive Hub API - Main Application

This is the main entry point for the FastAPI application.
It sets up the FastAPI instance, middleware, and routing.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Create FastAPI application instance
app = FastAPI(
    title=settings.project_name,
    description="A modern backend API built with FastAPI, SQLAlchemy, and PostgreSQL",
    version="1.0.0",
    debug=settings.debug,
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],  # Allow frontend origin
    allow_credentials=True,                 # Allow cookies and auth headers
    allow_methods=["*"],                    # Allow all HTTP methods
    allow_headers=["*"],                    # Allow all headers
)


@app.get("/")
async def root():
    """
    Root endpoint for basic health check
    
    Returns a welcome message and basic API information.
    """
    return {
        "message": f"Welcome to {settings.project_name}!",
        "status": "running",
        "environment": settings.environment,
        "api_docs": "/docs",
        "api_version": settings.api_v1_str,
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Returns the current status of the API service.
    Useful for monitoring and load balancer health checks.
    """
    return {
        "status": "healthy",
        "service": settings.project_name,
        "environment": settings.environment,
    }


# Include API routers
from app.api.v1.api import api_router
app.include_router(api_router, prefix=settings.api_v1_str)


# Development server startup
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug",
    ) 