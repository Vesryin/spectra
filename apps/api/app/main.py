"""
SpectraAI FastAPI Application - 2025 Edition
Modern async FastAPI backend with comprehensive AI integration capabilities.

Features:
- Async FastAPI with CORS and middleware
- WebSocket support for real-time communication
- Authentication integration ready
- AI chat endpoints with streaming
- Memory management API
- Health checks and monitoring
- Proper error handling and logging
"""

from __future__ import annotations

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.core.ai_manager import AIManager, ModelProvider
from app.routes import auth, chat, health, memory
from app.core.config import get_settings
from app.core.logging import setup_logging

# Initialize settings and logging
settings = get_settings()
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown tasks."""
    # Startup
    logger.info("🚀 Starting SpectraAI API server...")
    
    # Initialize AI Manager
    ai_manager = AIManager(
        provider=ModelProvider.OPENHERMES,
        model_name="openhermes-2.5-mistral-7b"
    )
    app.state.ai_manager = ai_manager
    
    # Initialize database connections (when implemented)
    # await init_database()
    
    logger.info("✅ SpectraAI API server started successfully")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down SpectraAI API server...")
    
    # Cleanup resources
    if hasattr(app.state, 'ai_manager'):
        await app.state.ai_manager.cleanup()
    
    logger.info("✅ SpectraAI API server shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="SpectraAI API",
    description="Advanced AI Assistant Backend with Emotional Intelligence",
    version="3.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "detail": str(exc) if settings.DEBUG else None,
        },
    )


# Include routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/chat", tags=["AI Chat"])
app.include_router(memory.router, prefix="/memory", tags=["Memory Management"])


# WebSocket connection manager
class ConnectionManager:
    """Manages WebSocket connections for real-time communication."""
    
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New WebSocket connection. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific WebSocket."""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: str):
        """Broadcast a message to all connected WebSockets."""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
                self.disconnect(connection)


# WebSocket connection manager instance
manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time AI chat."""
    await manager.connect(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            logger.info(f"Received message from {client_id}: {data}")
            
            # Process message with AI (placeholder for now)
            # ai_manager = app.state.ai_manager  # Will be used for actual AI processing
            
            # Echo back for now (will be replaced with actual AI processing)
            response = f"Echo from SpectraAI: {data}"
            await manager.send_personal_message(response, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"Client {client_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
        manager.disconnect(websocket)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "SpectraAI API",
        "version": "3.0.0",
        "description": "Advanced AI Assistant Backend with Emotional Intelligence",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "docs": "/docs" if settings.DEBUG else "disabled",
            "websocket": "/ws/{client_id}",
        },
    }


# Development server runner
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        access_log=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning",
    )
