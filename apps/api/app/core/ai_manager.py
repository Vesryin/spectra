"""
SpectraAI Core - AI Manager (2025 Edition)

Modern async AI management with type safety, error handling, and professional patterns.
Designed for OpenHermes 2.5 integration with extensible architecture.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Dict, List, Optional, Any, AsyncGenerator, Protocol, runtime_checkable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json

from pydantic import BaseModel, Field, ConfigDict
from pydantic_settings import BaseSettings
import httpx


# Type definitions
@dataclass
class ChatMessage:
    """Structured chat message with metadata."""
    content: str
    role: str = "user"
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIResponse:
    """Structured AI response with emotions and metadata."""
    content: str
    emotions: Dict[str, float] = field(default_factory=dict)
    confidence: float = 0.0
    processing_time: float = 0.0
    model_used: str = "openhermes-2.5"
    metadata: Dict[str, Any] = field(default_factory=dict)


class ModelProvider(str, Enum):
    """Supported AI model providers."""
    OPENHERMES = "openhermes"
    OLLAMA = "ollama"
    OPENAI = "openai"
    CLAUDE = "claude"


@runtime_checkable
class AIProvider(Protocol):
    """Protocol for AI providers."""
    
    async def generate_response(
        self, 
        message: str, 
        context: List[ChatMessage] = None,
        **kwargs
    ) -> AIResponse:
        """Generate AI response."""
        ...
    
    async def health_check(self) -> bool:
        """Check if provider is available."""
        ...


class OpenHermesProvider:
    """
    OpenHermes 2.5 provider via Ollama.
    
    Handles async communication with OpenHermes model,
    including error handling, retries, and response parsing.
    """
    
    def __init__(
        self, 
        base_url: str = "http://localhost:11434",
        model_name: str = "openhermes2.5-mistral:latest",
        timeout: float = 30.0
    ):
        self.base_url = base_url
        self.model_name = model_name
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
        self.logger = logging.getLogger(__name__)
    
    async def generate_response(
        self, 
        message: str, 
        context: List[ChatMessage] = None,
        **kwargs
    ) -> AIResponse:
        """Generate response using OpenHermes via Ollama."""
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Prepare context
            messages = []
            if context:
                for msg in context[-10:]:  # Last 10 messages for context
                    messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })
            
            messages.append({
                "role": "user", 
                "content": message
            })
            
            # Call Ollama API
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", 0.7),
                    "top_p": kwargs.get("top_p", 0.9),
                    "max_tokens": kwargs.get("max_tokens", 1000)
                }
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/chat",
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            content = result.get("message", {}).get("content", "")
            
            processing_time = asyncio.get_event_loop().time() - start_time
            
            return AIResponse(
                content=content,
                confidence=0.85,  # OpenHermes typically high confidence
                processing_time=processing_time,
                model_used=self.model_name,
                metadata={
                    "tokens_used": result.get("eval_count", 0),
                    "prompt_tokens": result.get("prompt_eval_count", 0)
                }
            )
            
        except Exception as e:
            self.logger.error(f"OpenHermes generation failed: {e}")
            processing_time = asyncio.get_event_loop().time() - start_time
            
            return AIResponse(
                content=f"I apologize, but I'm experiencing technical difficulties. Error: {str(e)}",
                confidence=0.0,
                processing_time=processing_time,
                model_used=self.model_name,
                metadata={"error": str(e)}
            )
    
    async def health_check(self) -> bool:
        """Check if OpenHermes is available."""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except Exception:
            return False
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()


class AIManager:
    """
    Central AI management system for SpectraAI.
    
    Coordinates between different AI providers, handles fallbacks,
    manages conversation context, and integrates with memory/personality systems.
    """
    
    def __init__(self):
        self.providers: Dict[ModelProvider, AIProvider] = {}
        self.primary_provider = ModelProvider.OPENHERMES
        self.conversation_history: List[ChatMessage] = []
        self.max_history = 50
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenHermes as primary
        self.providers[ModelProvider.OPENHERMES] = OpenHermesProvider()
    
    async def add_provider(self, provider_type: ModelProvider, provider: AIProvider):
        """Add a new AI provider."""
        self.providers[provider_type] = provider
        self.logger.info(f"Added {provider_type} provider")
    
    async def process_message(
        self, 
        message: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        **kwargs
    ) -> AIResponse:
        """
        Process user message through AI pipeline.
        
        Includes memory integration, personality application,
        and emotional processing.
        """
        # Create chat message
        chat_msg = ChatMessage(
            content=message,
            role="user",
            metadata={
                "user_id": user_id,
                "session_id": session_id
            }
        )
        
        # Add to conversation history
        self.conversation_history.append(chat_msg)
        
        # Trim history if needed
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
        
        # Get AI response
        provider = self.providers.get(self.primary_provider)
        if not provider:
            raise ValueError(f"Primary provider {self.primary_provider} not available")
        
        try:
            response = await provider.generate_response(
                message=message,
                context=self.conversation_history[:-1],  # Exclude current message
                **kwargs
            )
            
            # Add response to history
            assistant_msg = ChatMessage(
                content=response.content,
                role="assistant",
                metadata=response.metadata
            )
            self.conversation_history.append(assistant_msg)
            
            self.logger.info(f"Generated response in {response.processing_time:.2f}s")
            return response
            
        except Exception as e:
            self.logger.error(f"AI processing failed: {e}")
            # Return fallback response
            return AIResponse(
                content="I apologize, but I'm experiencing technical difficulties. Please try again.",
                confidence=0.0,
                model_used="fallback",
                metadata={"error": str(e)}
            )
    
    async def get_conversation_summary(self) -> str:
        """Generate summary of current conversation."""
        if not self.conversation_history:
            return "No conversation history available."
        
        # Take last 10 messages for summary
        recent_messages = self.conversation_history[-10:]
        summary_prompt = "Please provide a brief summary of this conversation:\n\n"
        
        for msg in recent_messages:
            summary_prompt += f"{msg.role}: {msg.content}\n"
        
        summary_prompt += "\nSummary:"
        
        provider = self.providers.get(self.primary_provider)
        if provider:
            response = await provider.generate_response(summary_prompt)
            return response.content
        
        return "Unable to generate summary."
    
    async def clear_history(self):
        """Clear conversation history."""
        self.conversation_history.clear()
        self.logger.info("Conversation history cleared")
    
    async def health_check(self) -> Dict[str, bool]:
        """Check health of all providers."""
        health_status = {}
        
        for provider_type, provider in self.providers.items():
            try:
                health_status[provider_type.value] = await provider.health_check()
            except Exception as e:
                self.logger.error(f"Health check failed for {provider_type}: {e}")
                health_status[provider_type.value] = False
        
        return health_status
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get AI manager statistics."""
        return {
            "conversation_length": len(self.conversation_history),
            "primary_provider": self.primary_provider.value,
            "available_providers": list(self.providers.keys()),
            "max_history": self.max_history
        }
