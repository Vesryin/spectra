# logic/ai_manager.py

"""
AI Manager - Orchestrates multiple AI providers with automatic fallback
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any
from pathlib import Path

from logic.ai_providers import create_provider, AIProvider
from config.settings import settings

logger = logging.getLogger(__name__)

class AIManager:
    """Manages multiple AI providers with automatic fallback."""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._load_default_config()
        self.providers: List[AIProvider] = []
        self.active_provider: Optional[AIProvider] = None
        self.fallback_provider: Optional[AIProvider] = None
        self.is_initialized = False
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration from settings."""
        return {
            'preferred_providers': getattr(settings, 'AI_PROVIDERS', ['local']),
            'fallback_provider': 'local',
            'providers': {
                'openai': {
                    'api_key': getattr(settings, 'OPENAI_API_KEY', ''),
                    'model': getattr(settings, 'OPENAI_MODEL', 'gpt-3.5-turbo'),
                    'max_tokens': getattr(settings, 'MAX_TOKENS', 300),
                    'temperature': getattr(settings, 'TEMPERATURE', 0.8)
                },
                'ollama': {
                    'base_url': getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434'),
                    'model': getattr(settings, 'OLLAMA_MODEL', 'openhermes'),
                    'max_tokens': getattr(settings, 'MAX_TOKENS', 300),
                    'temperature': getattr(settings, 'TEMPERATURE', 0.8)
                },
                'huggingface': {
                    'model': getattr(settings, 'HUGGINGFACE_MODEL', 'microsoft/DialoGPT-small'),
                    'max_tokens': getattr(settings, 'MAX_TOKENS', 200),
                    'temperature': getattr(settings, 'TEMPERATURE', 0.8)
                },
                'local': {
                    'max_tokens': getattr(settings, 'MAX_TOKENS', 300),
                    'temperature': getattr(settings, 'TEMPERATURE', 0.8)
                }
            }
        }
    
    async def initialize(self) -> bool:
        """Initialize AI providers in order of preference."""
        logger.info("🤖 Initializing AI Manager...")
        
        # Always create fallback provider first
        fallback_config = self.config['providers'].get('local', {})
        self.fallback_provider = create_provider('local', fallback_config)
        await self.fallback_provider.initialize()
        
        # Try to initialize preferred providers
        preferred = self.config.get('preferred_providers', ['local'])
        
        for provider_name in preferred:
            if provider_name == 'local':
                continue  # Already initialized as fallback
            
            try:
                provider_config = self.config['providers'].get(provider_name, {})
                provider = create_provider(provider_name, provider_config)
                
                logger.info(f"🔄 Trying to initialize {provider_name}...")
                
                if await provider.initialize():
                    self.providers.append(provider)
                    if not self.active_provider:
                        self.active_provider = provider
                        logger.info(f"✅ Active provider set to: {provider_name}")
                else:
                    logger.warning(f"⚠️ Failed to initialize {provider_name}")
                    
            except Exception as e:
                logger.error(f"❌ Error initializing {provider_name}: {e}")
        
        # If no preferred provider worked, use fallback
        if not self.active_provider:
            self.active_provider = self.fallback_provider
            logger.info("📱 Using local fallback provider")
        
        self.is_initialized = True
        logger.info(f"🎉 AI Manager initialized with {len(self.providers) + 1} providers")
        return True
    
    async def generate_response(self, prompt: str, context: Dict[str, str] = None) -> str:
        """Generate response with automatic fallback."""
        if not self.is_initialized:
            await self.initialize()
        
        context = context or {}
        
        # Try active provider first
        if self.active_provider and self.active_provider.is_available():
            try:
                response = await self.active_provider.generate_response(prompt, context)
                
                # Store in conversation history
                self.active_provider.add_to_history(prompt, response)
                
                return response
                
            except Exception as e:
                logger.error(f"❌ Active provider failed: {e}")
                logger.info("🔄 Falling back to next available provider...")
        
        # Try other providers
        for provider in self.providers:
            if provider == self.active_provider:
                continue
            
            if provider.is_available():
                try:
                    logger.info(f"🔄 Trying fallback provider: {type(provider).__name__}")
                    response = await provider.generate_response(prompt, context)
                    
                    # Update active provider
                    self.active_provider = provider
                    provider.add_to_history(prompt, response)
                    
                    return response
                    
                except Exception as e:
                    logger.error(f"❌ Fallback provider failed: {e}")
                    continue
        
        # Final fallback to local provider
        logger.info("🏠 Using final fallback (local provider)")
        response = await self.fallback_provider.generate_response(prompt, context)
        self.fallback_provider.add_to_history(prompt, response)
        
        return response
    
    def get_active_provider_info(self) -> Dict[str, Any]:
        """Get information about the currently active provider."""
        if not self.active_provider:
            return {"name": "none", "status": "not_initialized"}
        
        provider_name = type(self.active_provider).__name__.replace('Provider', '').lower()
        
        return {
            "name": provider_name,
            "status": "active" if self.active_provider.is_available() else "unavailable",
            "is_free": provider_name in ['local', 'huggingface', 'ollama'],
            "is_online": provider_name in ['openai'],
            "conversation_turns": len(self.active_provider.conversation_history)
        }
    
    def get_all_providers_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all providers."""
        status = {}
        
        # Check all initialized providers
        all_providers = self.providers + ([self.fallback_provider] if self.fallback_provider else [])
        
        for provider in all_providers:
            name = type(provider).__name__.replace('Provider', '').lower()
            status[name] = {
                "available": provider.is_available(),
                "initialized": provider.is_initialized,
                "is_active": provider == self.active_provider,
                "is_free": name in ['local', 'huggingface', 'ollama'],
                "conversation_turns": len(provider.conversation_history)
            }
        
        return status
    
    async def switch_provider(self, provider_name: str) -> bool:
        """Switch to a different provider."""
        target_provider = await self._find_or_create_provider(provider_name)
        
        if not target_provider:
            return False
        
        return self._activate_provider(target_provider, provider_name)
    
    def _find_existing_provider(self, provider_name: str) -> Optional[AIProvider]:
        """Find an existing provider by name."""
        if provider_name.lower() == 'local' and self.fallback_provider:
            return self.fallback_provider
        
        for provider in self.providers:
            if type(provider).__name__.lower().startswith(provider_name.lower()):
                return provider
        
        return None
    
    async def _create_new_provider(self, provider_name: str) -> Optional[AIProvider]:
        """Create and initialize a new provider."""
        if provider_name.lower() not in self.config['providers']:
            logger.error(f"Unknown provider: {provider_name}")
            return None
        
        config = self.config['providers'][provider_name.lower()]
        target_provider = create_provider(provider_name.lower(), config)
        
        if await target_provider.initialize():
            self.providers.append(target_provider)
            return target_provider
        else:
            logger.error(f"Failed to initialize {provider_name}")
            return None
    
    async def _find_or_create_provider(self, provider_name: str) -> Optional[AIProvider]:
        """Find existing provider or create new one."""
        target_provider = self._find_existing_provider(provider_name)
        
        if not target_provider:
            target_provider = await self._create_new_provider(provider_name)
        
        return target_provider
    
    def _activate_provider(self, provider: AIProvider, provider_name: str) -> bool:
        """Activate the given provider if available."""
        if provider.is_available():
            self.active_provider = provider
            logger.info(f"✅ Switched to provider: {provider_name}")
            return True
        else:
            logger.error(f"Provider {provider_name} is not available")
            return False
    
    async def test_all_providers(self) -> Dict[str, Dict[str, Any]]:
        """Test all providers with a simple prompt."""
        test_prompt = "Hello, this is a test message."
        results = {}
        
        all_providers = self.providers + ([self.fallback_provider] if self.fallback_provider else [])
        
        for provider in all_providers:
            name = type(provider).__name__.replace('Provider', '').lower()
            
            try:
                if provider.is_available():
                    start_time = asyncio.get_event_loop().time()
                    response = await provider.generate_response(test_prompt)
                    end_time = asyncio.get_event_loop().time()
                    
                    results[name] = {
                        "status": "success",
                        "response_time": round(end_time - start_time, 2),
                        "response_preview": response[:100] + "..." if len(response) > 100 else response,
                        "available": True
                    }
                else:
                    results[name] = {
                        "status": "unavailable",
                        "response_time": 0,
                        "response_preview": "",
                        "available": False
                    }
                    
            except Exception as e:
                results[name] = {
                    "status": "error",
                    "error": str(e),
                    "response_time": 0,
                    "response_preview": "",
                    "available": False
                }
        
        return results

# Singleton instance
_ai_manager_instance = None

def get_ai_manager() -> AIManager:
    """Get the singleton AI manager instance."""
    global _ai_manager_instance
    if _ai_manager_instance is None:
        _ai_manager_instance = AIManager()
    return _ai_manager_instance

async def initialize_ai() -> AIManager:
    """Initialize and return the AI manager."""
    manager = get_ai_manager()
    await manager.initialize()
    return manager
