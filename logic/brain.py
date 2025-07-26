# logic/brain.py

"""
Enhanced Brain Module for SpectraAI - Now with Universal AI Support
Uses the new AI Manager for automatic provider selection and fallback
"""

import logging
from typing import Dict, List, Optional, Any
import asyncio

from logic.ai_manager import get_ai_manager, initialize_ai
from config.settings import settings

logger = logging.getLogger(__name__)

class SpectraBrain:
    """Enhanced AI brain with universal provider support and intelligent responses."""
    
    def __init__(self):
        self.ai_manager = None
        self.conversation_context = []
        self.max_context_length = getattr(settings, 'MAX_CONTEXT_LENGTH', 10)
        self.system_persona = self._build_system_persona()
        self.is_initialized = False
    
    def _build_system_persona(self) -> str:
        """Build the system persona for SpectraAI."""
        return """You are SpectraAI, an advanced AI assistant with a dynamic personality system.

Key traits:
- Adaptive personality that evolves based on mood and interactions
- Emotional intelligence that responds to user emotions
- Self-reflective capabilities that learn from conversations
- Memory system that remembers important details
- Intelligent and engaging conversational style

Your responses should be:
- Natural and conversational
- Emotionally aware and empathetic  
- Contextually relevant to the conversation
- Reflective of your current personality state
- Helpful and informative while being personable

Remember: You have a memory system, emotional processing, and personality traits that should influence your responses."""
    
    async def initialize(self) -> bool:
        """Initialize the brain with AI providers."""
        if self.is_initialized:
            return True
        
        try:
            logger.info("🧠 Initializing SpectraBrain...")
            self.ai_manager = await initialize_ai()
            self.is_initialized = True
            
            # Log active provider info
            provider_info = self.ai_manager.get_active_provider_info()
            logger.info(f"🤖 Active AI Provider: {provider_info['name']} ({'FREE' if provider_info.get('is_free') else 'PAID'})")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize brain: {e}")
            return False
    
    async def think(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """
        Process user input and generate an intelligent response.
        
        Args:
            user_input: The user's message
            context: Additional context including personality, emotions, memory
            
        Returns:
            Generated response string
        """
        if not self.is_initialized:
            await self.initialize()
        
        try:
            # Build enhanced prompt with context
            enhanced_prompt = self._build_enhanced_prompt(user_input, context or {})
            
            # Generate response using AI manager
            response = await self.ai_manager.generate_response(enhanced_prompt, context)
            
            # Update conversation context
            self._update_conversation_context(user_input, response)
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Error in brain.think(): {e}")
            return self._generate_fallback_response(user_input)
    
    def _build_enhanced_prompt(self, user_input: str, context: Dict[str, Any]) -> str:
        """Build an enhanced prompt with personality, emotions, and memory context."""
        prompt_parts = [self.system_persona]
        
        self._add_personality_context(prompt_parts, context)
        self._add_emotional_context(prompt_parts, context)
        self._add_memory_context(prompt_parts, context)
        self._add_conversation_context(prompt_parts)
        
        # Add current user input
        prompt_parts.append(f"\nUser: {user_input}")
        prompt_parts.append("\nRespond as SpectraAI, incorporating your current personality and emotional state:")
        
        return "\n".join(prompt_parts)
    
    def _add_personality_context(self, prompt_parts: List[str], context: Dict[str, Any]):
        """Add personality context to prompt parts."""
        if 'personality' in context:
            personality = context['personality']
            prompt_parts.append("\nCurrent Personality State:")
            prompt_parts.append(f"- Mood: {personality.get('current_mood', 'neutral')}")
            prompt_parts.append(f"- Dominant Traits: {personality.get('dominant_traits', 'balanced')}")
    
    def _add_emotional_context(self, prompt_parts: List[str], context: Dict[str, Any]):
        """Add emotional context to prompt parts."""
        if 'emotions' in context:
            emotions = context['emotions']
            if emotions:
                prompt_parts.append("\nCurrent Emotional State:")
                for emotion, intensity in emotions.items():
                    prompt_parts.append(f"- {emotion.title()}: {intensity:.2f}")
    
    def _add_memory_context(self, prompt_parts: List[str], context: Dict[str, Any]):
        """Add memory context to prompt parts."""
        if 'relevant_memories' in context:
            memories = context['relevant_memories']
            if memories:
                prompt_parts.append("\nRelevant Memories:")
                for memory in memories[:3]:  # Limit to top 3 memories
                    prompt_parts.append(f"- {memory.get('content', 'No content')}")
    
    def _add_conversation_context(self, prompt_parts: List[str]):
        """Add conversation context to prompt parts."""
        if self.conversation_context:
            prompt_parts.append("\nRecent Conversation:")
            for turn in self.conversation_context[-3:]:  # Last 3 turns
                prompt_parts.append(f"User: {turn['user']}")
                prompt_parts.append(f"You: {turn['assistant']}")
    
    def _update_conversation_context(self, user_input: str, response: str):
        """Update the conversation context with the latest exchange."""
        self.conversation_context.append({
            'user': user_input,
            'assistant': response
        })
        
        # Keep context within limits
        if len(self.conversation_context) > self.max_context_length:
            self.conversation_context = self.conversation_context[-self.max_context_length:]
    
    def _generate_fallback_response(self, user_input: str) -> str:
        """Generate a fallback response when AI fails."""
        fallback_responses = [
            "I'm having trouble processing that right now. Could you rephrase your question?",
            "My systems are experiencing some difficulty. Let me try a different approach to help you.",
            "I'm encountering some technical challenges, but I'm still here to assist you.",
            "Let me think about that in a different way. Could you provide more context?",
            "I'm working through some processing issues, but I want to help. Can you be more specific?"
        ]
        
        # Simple hash-based selection for consistency
        index = hash(user_input) % len(fallback_responses)
        return fallback_responses[index]
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get status information about AI providers."""
        if not self.ai_manager:
            return {"status": "not_initialized"}
        
        return {
            "active_provider": self.ai_manager.get_active_provider_info(),
            "all_providers": self.ai_manager.get_all_providers_status(),
            "conversation_turns": len(self.conversation_context)
        }
    
    async def switch_ai_provider(self, provider_name: str) -> bool:
        """Switch to a different AI provider."""
        if not self.ai_manager:
            logger.error("AI Manager not initialized")
            return False
        
        success = await self.ai_manager.switch_provider(provider_name)
        if success:
            logger.info(f"✅ Brain switched to {provider_name} provider")
        return success
    
    async def test_all_providers(self) -> Dict[str, Any]:
        """Test all available AI providers."""
        if not self.ai_manager:
            return {"error": "AI Manager not initialized"}
        
        return await self.ai_manager.test_all_providers()
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the current conversation."""
        return {
            "total_turns": len(self.conversation_context),
            "context_length": self.max_context_length,
            "recent_topics": [turn['user'][:50] + "..." for turn in self.conversation_context[-5:]],
            "ai_provider": self.ai_manager.get_active_provider_info() if self.ai_manager else None
        }
    
    def clear_conversation(self):
        """Clear the conversation context."""
        self.conversation_context.clear()
        logger.info("🧹 Conversation context cleared")
    
    def shutdown(self):
        """Cleanup brain resources."""
        if self.ai_manager:
            # The AI manager handles its own cleanup
            pass
        self.conversation_context.clear()
        logger.info("🧠 SpectraBrain shutdown complete")

# Legacy compatibility functions
async def query_spectra(prompt: str, memory_context: str = None) -> str:
    """Legacy function for backward compatibility."""
    brain = get_brain()
    if not brain.is_initialized:
        await brain.initialize()
    
    context = {}
    if memory_context:
        context['memory_context'] = memory_context
    
    return await brain.think(prompt, context)

# Convenience function for global brain instance
_brain_instance = None

def get_brain() -> SpectraBrain:
    """Get the global brain instance."""
    global _brain_instance
    if _brain_instance is None:
        _brain_instance = SpectraBrain()
    return _brain_instance

# Legacy global instance for backward compatibility
brain = get_brain()