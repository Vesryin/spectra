# main.py

"""
SpectraAI - Advanced AI Assistant with Universal Provider Support
Enhanced with personality, memory, emotions, and multi-provider AI backends
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, Any

# Enhanced imports for all features
from core.personality import SpectraPersonality
from core.memory import SpectraMemory
from core.emotions import EmotionEngine
from core.reflection import ReflectionEngine
from logic.brain import get_brain
from config.settings import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SpectraAI:
    """
    Main SpectraAI class that orchestrates all components.
    Now with universal AI provider support!
    """
    
    def __init__(self):
        self.personality = SpectraPersonality()
        self.memory = SpectraMemory()
        self.emotions = EmotionEngine()
        self.reflection = ReflectionEngine()
        self.brain = get_brain()
        self.is_running = False
        self.conversation_count = 0
    
    async def initialize(self) -> bool:
        """Initialize all SpectraAI components."""
        try:
            logger.info("🚀 Initializing SpectraAI...")
            
            # Initialize brain with AI providers
            if not await self.brain.initialize():
                logger.error("❌ Failed to initialize brain")
                return False
            
            # Initialize other components
            self.memory.initialize()
            self.emotions.initialize()
            
            logger.info("✅ SpectraAI initialized successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize SpectraAI: {e}")
            return False
    
    def display_startup_info(self):
        """Display startup information and AI provider status."""
        print("\n" + "="*60)
        print("🌟 SpectraAI - Universal AI Assistant")
        print("="*60)
        
        # Show personality
        personality_info = self.personality.get_current_state()
        print(f"👤 Personality: {personality_info.get('current_mood', 'Unknown').title()} mood")
        
        # Show AI provider status
        provider_status = self.brain.get_provider_status()
        active_provider = provider_status.get('active_provider', {})
        provider_name = active_provider.get('name', 'unknown')
        is_free = active_provider.get('is_free', False)
        cost_info = "FREE 🆓" if is_free else "PAID 💰"
        
        print(f"🤖 AI Provider: {provider_name.upper()} ({cost_info})")
        print(f"💭 Memory: {self.memory.get_memory_count()} stored memories")
        print("😊 Emotions: Active and responsive")
        print("="*60)
        
        if is_free:
            print("💡 You're using a FREE AI provider - no API costs!")
        
        print("\nType 'help' for commands, 'quit' to exit")
        print("How can I assist you today?\n")
    
    async def process_user_input(self, user_input: str) -> str:
        """Process user input through all SpectraAI systems."""
        
        # Handle special commands
        if user_input.lower() in ['quit', 'exit', 'bye']:
            return "EXIT_COMMAND"
        
        if user_input.lower() == 'help':
            return self._get_help_text()
        
        if user_input.lower().startswith('/'):
            return await self._handle_command(user_input)
        
        # Process through all systems
        try:
            # 1. Store in memory
            self.memory.store_interaction(user_input, "user")
            
            # 2. Analyze emotions
            user_emotions = self.emotions.analyze_text(user_input)
            self.emotions.update_state(user_emotions)
            
            # 3. Get relevant memories
            relevant_memories = self.memory.get_relevant_memories(user_input, limit=3)
            
            # 4. Build context for brain
            context = {
                'personality': self.personality.get_current_state(),
                'emotions': self.emotions.get_emotional_state(),
                'relevant_memories': relevant_memories,
                'user_emotions': user_emotions
            }
            
            # 5. Generate response using enhanced brain
            response = await self.brain.think(user_input, context)
            
            # 6. Store AI response in memory
            self.memory.store_interaction(response, "assistant")
            
            # 7. Update personality based on interaction
            self.personality.update_from_interaction(user_input, response)
            
            # 8. Reflect on conversation periodically
            self.conversation_count += 1
            if self.conversation_count % 5 == 0:
                await self._perform_reflection()
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Error processing input: {e}")
            return "I'm experiencing some technical difficulties. Let me try to help you anyway!"
    
    def _get_help_text(self) -> str:
        """Get help text for user commands."""
        return """
🆘 SpectraAI Commands:
─────────────────────
• /status     - Show AI provider and system status
• /memory     - View recent memories
• /emotions   - Show current emotional state  
• /personality - View personality state
• /providers  - List all AI providers
• /switch [provider] - Switch AI provider
• /test       - Test all AI providers
• /clear      - Clear conversation history
• /reflection - Show recent reflections
• help        - Show this help message
• quit/exit   - Exit SpectraAI

💡 Tips:
• I remember our conversations and learn from them
• My personality and emotions adapt based on our interactions
• You can switch between free and paid AI providers anytime
"""
    
    async def _handle_command(self, command: str) -> str:
        """Handle special user commands."""
        cmd = command[1:].lower().strip()
        
        if cmd == 'status':
            return self._get_status_info()
        
        elif cmd == 'memory':
            return self._get_memory_info()
        
        elif cmd == 'emotions':
            return self._get_emotions_info()
        
        elif cmd == 'personality':
            return self._get_personality_info()
        
        elif cmd == 'providers':
            return self._get_providers_info()
        
        elif cmd.startswith('switch '):
            provider_name = cmd[7:].strip()
            return await self._switch_provider(provider_name)
        
        elif cmd == 'test':
            return await self._test_providers()
        
        elif cmd == 'clear':
            return self._clear_conversation()
        
        elif cmd == 'reflection':
            return self._get_reflection_info()
        
        else:
            return "❓ Unknown command. Type 'help' for available commands."
    
    def _get_status_info(self) -> str:
        """Get system status information."""
        provider_status = self.brain.get_provider_status()
        active_provider = provider_status.get('active_provider', {})
        
        status = f"""
📊 SpectraAI Status:
───────────────────
🤖 AI Provider: {active_provider.get('name', 'Unknown')}
💰 Cost: {'FREE' if active_provider.get('is_free') else 'PAID'}
🔗 Status: {'Online' if active_provider.get('status') == 'active' else 'Offline'}
💭 Memory Count: {self.memory.get_memory_count()}
😊 Emotional State: {len(self.emotions.get_emotional_state())} active emotions
🎭 Current Mood: {self.personality.get_current_state().get('current_mood', 'neutral')}
💬 Conversation Turns: {provider_status.get('conversation_turns', 0)}
"""
        return status
    
    def _get_memory_info(self) -> str:
        """Get memory information."""
        recent_memories = self.memory.get_recent_memories(5)
        
        info = "🧠 Recent Memories:\n"
        info += "─────────────────\n"
        
        for i, memory in enumerate(recent_memories, 1):
            content = memory.get('content', 'No content')[:60]
            info += f"{i}. {content}...\n"
        
        info += f"\nTotal memories: {self.memory.get_memory_count()}"
        return info
    
    def _get_emotions_info(self) -> str:
        """Get emotional state information."""
        emotions = self.emotions.get_emotional_state()
        
        info = "😊 Current Emotional State:\n"
        info += "─────────────────────────\n"
        
        if emotions:
            for emotion, intensity in emotions.items():
                bar = "█" * int(intensity * 10)
                info += f"{emotion.title()}: {bar} ({intensity:.2f})\n"
        else:
            info += "No active emotions detected."
        
        return info
    
    def _get_personality_info(self) -> str:
        """Get personality state information."""
        personality = self.personality.get_current_state()
        
        info = "🎭 Personality State:\n"
        info += "──────────────────\n"
        info += f"Mood: {personality.get('current_mood', 'neutral').title()}\n"
        info += f"Dominant Traits: {personality.get('dominant_traits', 'balanced')}\n"
        info += f"Energy Level: {personality.get('energy_level', 'moderate')}\n"
        
        return info
    
    def _get_providers_info(self) -> str:
        """Get AI providers information."""
        all_providers = self.brain.get_provider_status().get('all_providers', {})
        
        info = "🤖 Available AI Providers:\n"
        info += "─────────────────────────\n"
        
        for name, status in all_providers.items():
            icon = "✅" if status.get('available') else "❌"
            cost = "FREE" if status.get('is_free') else "PAID"
            active = " (ACTIVE)" if status.get('is_active') else ""
            info += f"{icon} {name.upper()}: {cost}{active}\n"
        
        return info
    
    async def _switch_provider(self, provider_name: str) -> str:
        """Switch to a different AI provider."""
        try:
            success = await self.brain.switch_ai_provider(provider_name)
            if success:
                return f"✅ Switched to {provider_name} provider"
            else:
                return f"❌ Failed to switch to {provider_name} provider"
        except Exception as e:
            return f"❌ Error switching provider: {e}"
    
    async def _test_providers(self) -> str:
        """Test all AI providers."""
        try:
            results = await self.brain.test_all_providers()
            
            info = "🧪 AI Provider Test Results:\n"
            info += "────────────────────────\n"
            
            for name, result in results.items():
                status = result.get('status', 'unknown')
                if status == 'success':
                    time = result.get('response_time', 0)
                    info += f"✅ {name.upper()}: OK ({time}s)\n"
                elif status == 'unavailable':
                    info += f"⚠️ {name.upper()}: Unavailable\n"
                else:
                    error = result.get('error', 'Unknown error')
                    info += f"❌ {name.upper()}: {error}\n"
            
            return info
            
        except Exception as e:
            return f"❌ Error testing providers: {e}"
    
    def _clear_conversation(self) -> str:
        """Clear conversation history."""
        self.brain.clear_conversation()
        self.conversation_count = 0
        return "🧹 Conversation history cleared!"
    
    def _get_reflection_info(self) -> str:
        """Get reflection information."""
        reflections = self.reflection.get_recent_reflections(3)
        
        info = "🤔 Recent Reflections:\n"
        info += "────────────────────\n"
        
        for i, reflection in enumerate(reflections, 1):
            content = reflection.get('insight', 'No insight')[:80]
            info += f"{i}. {content}...\n"
        
        return info
    
    async def _perform_reflection(self):
        """Perform periodic self-reflection."""
        try:
            recent_memories = self.memory.get_recent_memories(10)
            current_emotions = self.emotions.get_emotional_state()
            
            if recent_memories:
                reflection_context = {
                    'recent_interactions': recent_memories,
                    'emotional_state': current_emotions,
                    'conversation_count': self.conversation_count
                }
                
                await self.reflection.reflect_on_interactions(reflection_context)
                logger.info("🤔 Performed periodic self-reflection")
        
        except Exception as e:
            logger.error(f"❌ Error during reflection: {e}")
    
    async def run(self):
        """Main conversation loop for SpectraAI."""
        
        # Initialize all systems
        if not await self.initialize():
            print("❌ Failed to initialize SpectraAI. Exiting.")
            return
        
        # Display startup info
        self.display_startup_info()
        
        # Main conversation loop
        self.is_running = True
        
        try:
            while self.is_running:
                try:
                    # Get user input
                    user_input = await asyncio.to_thread(input, "🔵 You: ")
                    user_input = user_input.strip()
                    
                    if not user_input:
                        continue
                    
                    # Process input
                    response = await self.process_user_input(user_input)
                    
                    # Handle exit command
                    if response == "EXIT_COMMAND":
                        print("🌟 SpectraAI: Thank you for our conversation! Take care! 👋")
                        break
                    
                    # Display response
                    print(f"🤖 SpectraAI: {response}\n")
                    
                except KeyboardInterrupt:
                    print("\n\n🌟 SpectraAI: Goodbye! It was wonderful talking with you! 👋")
                    break
                    
                except Exception as e:
                    logger.error(f"❌ Error in conversation loop: {e}")
                    print("❌ I encountered an error. Let me try to continue our conversation.\n")
                    continue
        
        finally:
            # Cleanup
            self.brain.shutdown()
            logger.info("🔚 SpectraAI session ended")

async def main():
    """Main entry point for SpectraAI."""
    try:
        spectra = SpectraAI()
        await spectra.run()
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        print(f"❌ Fatal error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Run the async main function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error starting SpectraAI: {e}")
        sys.exit(1)