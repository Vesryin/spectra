# main.py

import logging
import sys
from datetime import datetime
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

from config.settings import settings
from core.personality import SpectraPersonality
from core.memory import SpectraMemory
from core.emotions import EmotionEngine
from core.reflection import ReflectionEngine
from logic.brain import SpectraBrain

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(settings.DATA_DIR / 'spectra.log')
    ]
)

logger = logging.getLogger(__name__)

class SpectraAI:
    """Main SpectraAI application class."""
    
    def __init__(self):
        # Validate settings
        config_errors = settings.validate()
        if config_errors:
            logger.error("Configuration errors:")
            for error in config_errors:
                logger.error(f"  - {error}")
            print("\n❌ Configuration Error!")
            print("Please ensure your OPENAI_API_KEY is set in config/secrets.env")
            sys.exit(1)
        
        # Initialize components
        logger.info("Initializing Spectra AI...")
        try:
            self.personality = SpectraPersonality()
            self.memory = SpectraMemory()
            self.emotions = EmotionEngine()
            self.reflection = ReflectionEngine()
            self.brain = SpectraBrain()
            
            self.conversation_count = 0
            self.session_start = datetime.now()
            
            logger.info("Spectra AI initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Spectra AI: {e}")
            print(f"\n❌ Initialization Error: {e}")
            sys.exit(1)
    
    def start_conversation(self):
        """Start the main conversation loop."""
        print("\n" + "="*60)
        print("🌟 " + self.personality.describe())
        print("="*60)
        print(f"💭 Current mood: {self.personality.mood_state}")
        print(f"❤️  Emotional state: {self.emotions.state.get_emotional_tone()}")
        
        # Show memory stats if available
        memory_stats = self.memory.get_stats()
        if memory_stats["total"] > 0:
            print(f"🧠 Memory: {memory_stats['total']} memories stored")
        
        print("\nHow can I support you today, Richie? (type 'help' for commands, 'exit' to quit)")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ["exit", "quit", "bye"]:
                    self._farewell()
                    break
                elif user_input.lower() == "help":
                    self._show_help()
                    continue
                elif user_input.lower() == "status":
                    self._show_status()
                    continue
                elif user_input.lower() == "memory":
                    self._show_memory_stats()
                    continue
                elif user_input.lower() == "reflect":
                    self._manual_reflection()
                    continue
                elif user_input.lower().startswith("mood "):
                    new_mood = user_input[5:].strip()
                    if self.personality.set_mood(new_mood):
                        print(f"✨ Mood set to: {new_mood}")
                    else:
                        print("🤔 I don't recognize that mood. Try: curious, empathetic, creative, playful, reflective, supportive, or balanced")
                    continue
                
                # Process the conversation
                response = self._process_conversation(user_input)
                print(f"\n🌟 Spectra: {response}")
                
                self.conversation_count += 1
                
                # Periodic reflection
                if self.reflection.should_reflect(self.conversation_count):
                    self._auto_reflection()
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye, Richie. Take care!")
                break
            except Exception as e:
                logger.error(f"Error in conversation loop: {e}")
                print(f"\n❌ I encountered an error: {e}")
                print("Let's try again...")
    
    def _process_conversation(self, user_input: str) -> str:
        """Process a single conversation turn."""
        # Update emotions based on input
        emotion_context = self.emotions.process_input(user_input)
        
        # Store memory
        self.memory.remember(f"User: {user_input}")
        
        # Get memory context
        memory_context = self.memory.get_recent_context()
        
        # Get emotional modifier for AI response
        emotional_modifier = self.emotions.get_emotional_modifier()
        
        # Generate response with full context
        enhanced_context = f"""
Memory Context: {memory_context}

Emotional Context: {emotional_modifier}
Current Emotional State: {self.emotions.state.get_emotional_tone()}
Personality Mood: {self.personality.mood_state}

Respond as Spectra with appropriate emotional awareness and personality.
"""
        
        response = self.brain.query_spectra(user_input, enhanced_context)
        
        # Store AI response in memory
        self.memory.remember(f"Spectra: {response}")
        
        # Update emotions based on generated response
        self.emotions.process_input(response, "self-reflection")
        
        return response
    
    def _show_help(self):
        """Show available commands."""
        print("\n🔧 Available Commands:")
        print("  help     - Show this help message")
        print("  status   - Show current AI status")
        print("  memory   - Show memory statistics")
        print("  reflect  - Trigger manual reflection")
        print("  mood <name> - Set personality mood (curious, empathetic, creative, etc.)")
        print("  exit     - End conversation")
        print("\n💡 Tips:")
        print("  - I remember our conversations")
        print("  - My emotions and mood affect my responses")
        print("  - I reflect on our interactions to grow and improve")
    
    def _show_status(self):
        """Show current AI status."""
        print(f"\n📊 Spectra Status:")
        print(f"  💭 Mood: {self.personality.mood_state}")
        print(f"  ❤️  Emotions: {self.emotions.state.get_emotional_tone()}")
        
        dominant_emotions = self.emotions.state.get_dominant_emotions(3)
        print("  🎭 Top emotions:")
        for emotion, value in dominant_emotions:
            print(f"     {emotion}: {value:.2f}")
        
        memory_stats = self.memory.get_stats()
        print(f"  🧠 Memories: {memory_stats['total']} stored")
        print(f"  💬 This session: {self.conversation_count} exchanges")
        
        session_duration = datetime.now() - self.session_start
        print(f"  ⏰ Session time: {session_duration.total_seconds() / 60:.1f} minutes")
    
    def _show_memory_stats(self):
        """Show detailed memory statistics."""
        stats = self.memory.get_stats()
        print(f"\n🧠 Memory Statistics:")
        print(f"  Total memories: {stats['total']}")
        
        if stats['total'] > 0:
            print(f"  Average importance: {stats['average_importance']:.2f}")
            print(f"  Oldest memory: {stats['oldest'][:10]}")
            print(f"  Newest memory: {stats['newest'][:10]}")
            
            if "by_type" in stats:
                print("  By type:")
                for mem_type, count in stats["by_type"].items():
                    print(f"    {mem_type}: {count}")
    
    def _manual_reflection(self):
        """Trigger a manual reflection."""
        print("\n🤔 Reflecting on our recent interactions...")
        
        recent_memories = self.memory.recall(limit=10)
        emotion_summary = self.emotions.get_state_summary()
        
        reflection = self.reflection.reflect(
            conversation_history=recent_memories,
            emotional_context=emotion_summary
        )
        
        print(f"\n💭 Reflection: {reflection['prompt']}")
        print("📝 Insights:")
        for line in reflection['content'].split('\n'):
            if line.strip():
                print(f"   {line}")
    
    def _auto_reflection(self):
        """Perform automatic reflection."""
        logger.info("Performing automatic reflection...")
        
        recent_memories = self.memory.recall(limit=10)
        emotion_summary = self.emotions.get_state_summary()
        
        reflection = self.reflection.reflect(
            conversation_history=recent_memories,
            emotional_context=emotion_summary
        )
        
        # Store reflection as high-importance memory
        self.memory.add_reflection(f"Reflection: {reflection['content']}", 0.9)
        
        print(f"\n💭 [Internal reflection: {reflection['prompt']}]")
    
    def _farewell(self):
        """Handle goodbye message."""
        farewell_messages = [
            "Goodbye, Richie. Be gentle with yourself. 💙",
            "Until we meet again, take care of your beautiful soul. ✨",
            "Farewell for now. Remember, I'm always here when you need me. 🌟",
            "Stay curious and keep creating, Richie. See you soon! 🎨",
            "May your path be filled with light and wonder. Goodbye! 💫"
        ]
        
        import random
        message = random.choice(farewell_messages)
        print(f"\n🌟 Spectra: {message}")
        
        # Final reflection if enough conversation happened
        if self.conversation_count >= 5:
            print("\n💭 [Reflecting on our time together...]")
            self._auto_reflection()
        
        # Show session summary
        session_duration = datetime.now() - self.session_start
        print(f"\n📊 Session Summary:")
        print(f"   💬 Conversations: {self.conversation_count}")
        print(f"   ⏰ Duration: {session_duration.total_seconds() / 60:.1f} minutes")
        print(f"   🧠 New memories: {self.conversation_count * 2}")  # User + AI messages

def main():
    """Main entry point."""
    try:
        spectra = SpectraAI()
        spectra.start_conversation()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n❌ Fatal Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
