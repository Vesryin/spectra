"""
SpectraAI API - Modern FastAPI Server (2025)
Professional-grade API with OpenHermes integration
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
import asyncio
import json
import logging
from datetime import datetime
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Pydantic models for request/response validation
class ChatMessage(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime
    emotions: Dict[str, float]
    memory_updated: bool

class MemoryEntry(BaseModel):
    id: str
    content: str
    timestamp: datetime
    importance: float
    tags: List[str]

class PersonalityConfig(BaseModel):
    traits: Dict[str, float]
    response_style: str
    creativity: float = Field(ge=0.0, le=1.0)

# Modern FastAPI app with metadata
app = FastAPI(
    title="SpectraAI API",
    description="Advanced AI Assistant with Memory, Emotions, and Personality",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Modern CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "https://*.pages.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import SpectraAI core modules
try:
    import sys
    sys.path.append(str(Path(__file__).parent.parent / "spectra-core" / "src"))
    
    from ai_manager import AIManager
    from emotions import EmotionSystem
    from memory import MemorySystem
    from personality import PersonalitySystem
    from brain import Brain
    
    logger.info("SpectraAI core modules loaded successfully")
except ImportError as e:
    logger.error(f"Failed to import SpectraAI modules: {e}")
    # Create mock classes for development
    class AIManager:
        async def process_message(self, message: str) -> str:
            return f"Mock response to: {message}"
    
    class EmotionSystem:
        def get_current_emotions(self) -> Dict[str, float]:
            return {"happy": 0.7, "excited": 0.5}
    
    class MemorySystem:
        def add_memory(self, content: str) -> bool:
            return True
        
        def search_memories(self, query: str) -> List[Dict]:
            return []
    
    class PersonalitySystem:
        def get_traits(self) -> Dict[str, float]:
            return {"openness": 0.8, "creativity": 0.9}
    
    class Brain:
        def __init__(self):
            self.ai_manager = AIManager()
            self.emotions = EmotionSystem()
            self.memory = MemorySystem()
            self.personality = PersonalitySystem()

# Initialize SpectraAI
brain = Brain()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# API Routes

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>SpectraAI API</title>
        </head>
        <body>
            <h1>SpectraAI API - 2025 Edition</h1>
            <p>Welcome to the SpectraAI Advanced AI Assistant API</p>
            <ul>
                <li><a href="/docs">API Documentation</a></li>
                <li><a href="/health">Health Check</a></li>
                <li><a href="/status">System Status</a></li>
            </ul>
        </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "2.0.0",
        "ai_system": "operational"
    }

@app.get("/status")
async def system_status():
    """Detailed system status"""
    try:
        emotions = brain.emotions.get_current_emotions()
        personality = brain.personality.get_traits()
        
        return {
            "status": "operational",
            "timestamp": datetime.now(),
            "components": {
                "ai_manager": "healthy",
                "emotions": "active",
                "memory": "connected",
                "personality": "configured"
            },
            "current_state": {
                "emotions": emotions,
                "personality_traits": personality
            },
            "connections": len(manager.active_connections)
        }
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail="System status check failed")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    """Main chat endpoint with SpectraAI"""
    try:
        logger.info(f"Processing message: {message.content[:50]}...")
        
        # Process message through SpectraAI brain
        response = await brain.ai_manager.process_message(message.content)
        
        # Add to memory
        memory_updated = brain.memory.add_memory(message.content)
        
        # Get current emotional state
        emotions = brain.emotions.get_current_emotions()
        
        return ChatResponse(
            response=response,
            timestamp=datetime.now(),
            emotions=emotions,
            memory_updated=memory_updated
        )
        
    except Exception as e:
        logger.error(f"Chat processing failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to process message")

@app.get("/memory", response_model=List[MemoryEntry])
async def get_memories(limit: int = 50, search: Optional[str] = None):
    """Retrieve memories with optional search"""
    try:
        if search:
            memories = brain.memory.search_memories(search)
        else:
            memories = brain.memory.get_recent_memories(limit)
        
        return [
            MemoryEntry(
                id=mem.get("id", ""),
                content=mem.get("content", ""),
                timestamp=mem.get("timestamp", datetime.now()),
                importance=mem.get("importance", 0.5),
                tags=mem.get("tags", [])
            )
            for mem in memories
        ]
    except Exception as e:
        logger.error(f"Memory retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve memories")

@app.get("/personality", response_model=PersonalityConfig)
async def get_personality():
    """Get current personality configuration"""
    try:
        traits = brain.personality.get_traits()
        return PersonalityConfig(
            traits=traits,
            response_style=traits.get("response_style", "balanced"),
            creativity=traits.get("creativity", 0.7)
        )
    except Exception as e:
        logger.error(f"Personality retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve personality")

@app.put("/personality", response_model=PersonalityConfig)
async def update_personality(config: PersonalityConfig):
    """Update personality configuration"""
    try:
        # Update personality system
        success = brain.personality.update_traits(config.traits)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to update personality")
        
        return config
    except Exception as e:
        logger.error(f"Personality update failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to update personality")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await manager.connect(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process through SpectraAI
            response = await brain.ai_manager.process_message(message_data["content"])
            emotions = brain.emotions.get_current_emotions()
            
            # Send response back
            response_data = {
                "type": "chat_response",
                "response": response,
                "emotions": emotions,
                "timestamp": datetime.now().isoformat()
            }
            
            await manager.send_personal_message(json.dumps(response_data), websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("SpectraAI API starting up...")
    logger.info("System initialized successfully")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("SpectraAI API shutting down...")

if __name__ == "__main__":
    # Development server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
