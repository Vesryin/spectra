"""
Health Check Routes
System health monitoring and status endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import asyncio
import psutil
import time
from datetime import datetime

from app.core.config import get_settings

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: datetime
    version: str
    environment: str
    uptime: float
    system: Dict[str, Any]


class DatabaseHealthResponse(BaseModel):
    """Database health response model."""
    status: str
    response_time_ms: float
    connection_pool: Dict[str, Any]


@router.get("/", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint."""
    settings = get_settings()
    
    # Calculate uptime (placeholder for now)
    uptime = time.time() - 1700000000  # Replace with actual start time
    
    # System information
    system_info = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "platform": psutil.uname().system,
    }
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="3.0.0",
        environment=settings.ENVIRONMENT,
        uptime=uptime,
        system=system_info,
    )


@router.get("/live")
async def liveness_probe():
    """Kubernetes liveness probe endpoint."""
    return {"status": "alive", "timestamp": datetime.now()}


@router.get("/ready")
async def readiness_probe():
    """Kubernetes readiness probe endpoint."""
    # Check critical dependencies
    checks = {
        "api": True,  # API is running if we reach this point
        "database": await check_database_health(),
        "ai_service": await check_ai_service_health(),
    }
    
    all_ready = all(checks.values())
    
    return {
        "status": "ready" if all_ready else "not_ready",
        "checks": checks,
        "timestamp": datetime.now(),
    }


@router.get("/database", response_model=DatabaseHealthResponse)
async def database_health():
    """Database connection health check."""
    start_time = time.time()
    
    try:
        # Placeholder for actual database connection check
        await asyncio.sleep(0.01)  # Simulate database query
        
        response_time = (time.time() - start_time) * 1000
        
        return DatabaseHealthResponse(
            status="healthy",
            response_time_ms=response_time,
            connection_pool={
                "active_connections": 5,
                "idle_connections": 3,
                "max_connections": 20,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database health check failed: {str(e)}"
        )


async def check_database_health() -> bool:
    """Check database connectivity."""
    try:
        # Placeholder for actual database health check
        await asyncio.sleep(0.001)
        return True
    except Exception:
        return False


async def check_ai_service_health() -> bool:
    """Check AI service connectivity."""
    try:
        # Placeholder for actual AI service health check
        await asyncio.sleep(0.001)
        return True
    except Exception:
        return False
