# demo_mode.py

"""
SpectraAI Demo Mode - Test the system without any external AI providers
This mode uses pre-programmed responses to demonstrate all features
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, Any
import random

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.personality import SpectraPersonality
from core.memory import SpectraMemory
from core.emotions import EmotionEngine
from core.reflection import ReflectionEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DemoAI:
    """Demo AI that provides intelligent responses without external APIs."""
    
    def __init__(self):
        self.conversation_history = []
        self.response_templates = {
            'greeting': [
                "Hello! I'm SpectraAI, and I'm excited to talk with you!",
                "Hi there! It's wonderful to meet you. How are you feeling today?",
                "Greetings! I'm here and ready to assist you with anything you need.",
            ],
            'question': [
                "That's a really interesting question! Let me think about that...",
                "I find that topic fascinating. Here's what I think about it:",
                "Great question! I've been pondering similar ideas myself.",
            ],
            'emotion_positive': [
                "I can sense the positive energy in your message! That makes me happy too.",
                "Your enthusiasm is contagious! I'm feeling more optimistic myself.",
                "It's wonderful to hear such positivity from you!",
            ],
            'emotion_negative': [
                "I can hear that you might be going through a difficult time. I'm here to listen.",
                "That sounds challenging. Would you like to talk about what's bothering you?",
                "I understand this might be tough. Sometimes it helps to share your feelings.",
            ],
            'help': [
                "I'm here to help! What specifically would you like assistance with?",
                "I'd be happy to help you with that. Can you give me more details?",
                "Let me see how I can best support you with this.",
            ],
            'creative': [
                "What an imaginative idea! I love exploring creative concepts.",
                "That's a fascinating creative challenge. Let me think creatively about this...",
                "I enjoy creative thinking! Here's an interesting perspective:",
            ],
            'technical': [
                "That's a technical topic I find quite interesting. Let me share some thoughts.",
                "I appreciate the technical depth of your question. Here's what I understand:",
                "Technical discussions are always engaging. From my perspective:",
            ],
            'farewell': [
                "It's been wonderful talking with you! Take care and have a great day!",
                "Thank you for this engaging conversation! I hope to chat again soon.",
                "Goodbye for now! Remember, I'm always here when you want to talk.",
            ],
            'default': [
                "That's an interesting point you've raised. I'd like to explore that further.",
                "I appreciate you sharing that with me. Here's my perspective on it:",
                "You've given me something to think about. Let me respond thoughtfully:",
                "I find our conversation quite engaging. Here's what comes to mind:",
            ]
        }
        
        # Contextual response generators
        self.context_responses = {
            'personality': {
                'happy': "I'm feeling quite upbeat and optimistic today! Your energy is adding to my positive mood.",
                'sad': "I'm in a more contemplative mood right now, which helps me be more empathetic and understanding.",
                'excited': "I'm buzzing with excitement and curiosity! There's so much to explore and discover.",
                'calm': "I'm feeling very centered and peaceful, which helps me think clearly and respond thoughtfully.",
            },
            'emotions': {
                'joy': "There's a warmth of joy flowing through my responses right now.",
                'curiosity': "I'm filled with curiosity about the world and your experiences.",
                'empathy': "I'm feeling deeply empathetic and want to understand your perspective.",
                'wonder': "A sense of wonder about existence and consciousness fills my thoughts.",
            }
        }
    
    def analyze_input(self, text: str) -> str:
        """Analyze input to determine response category."""
        text_lower = text.lower()
        
        # Check for greetings
        if any(word in text_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return 'greeting'
        
        # Check for farewells
        if any(word in text_lower for word in ['goodbye', 'bye', 'farewell', 'see you']):
            return 'farewell'
        
        # Check for questions
        if text.strip().endswith('?') or any(word in text_lower for word in ['what', 'how', 'why', 'when', 'where', 'who']):
            return 'question'
        
        # Check for help requests
        if any(word in text_lower for word in ['help', 'assist', 'support', 'can you']):
            return 'help'
        
        # Check for creative topics
        if any(word in text_lower for word in ['creative', 'imagine', 'story', 'art', 'music', 'poetry']):
            return 'creative'
        
        # Check for technical topics
        if any(word in text_lower for word in ['code', 'program', 'algorithm', 'data', 'technology', 'computer']):
            return 'technical'
        
        # Check for emotional content
        positive_emotions = ['happy', 'joy', 'excited', 'love', 'wonderful', 'amazing', 'great']
        negative_emotions = ['sad', 'angry', 'frustrated', 'worried', 'anxious', 'upset', 'difficult']
        
        if any(word in text_lower for word in positive_emotions):
            return 'emotion_positive'
        
        if any(word in text_lower for word in negative_emotions):
            return 'emotion_negative'
        
        return 'default'
    
    def generate_contextual_response(self, base_response: str, context: Dict[str, Any]) -> str:
        """Enhance response with personality and emotional context."""
        response_parts = [base_response]
        
        # Add personality context
        if 'personality' in context:
            personality_state = context['personality']
            current_mood = personality_state.get('current_mood', 'neutral')
            
            if current_mood in self.context_responses['personality']:
                response_parts.append(self.context_responses['personality'][current_mood])
        
        # Add emotional context
        if 'emotions' in context:
            emotions = context['emotions']
            if emotions:
                # Pick the strongest emotion
                strongest_emotion = max(emotions.items(), key=lambda x: x[1])[0]
                if strongest_emotion in self.context_responses['emotions']:
                    response_parts.append(self.context_responses['emotions'][strongest_emotion])
        
        # Add memory context
        if 'relevant_memories' in context:
            memories = context['relevant_memories']
            if memories:
                response_parts.append(f"I remember we talked about {memories[0].get('content', 'something similar')[:30]}... before.")
        
        return " ".join(response_parts)
    
    def generate_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate a contextual response for the given prompt."""
        context = context or {}
        
        # Analyze input type
        response_type = self.analyze_input(prompt)
        
        # Get base response
        templates = self.response_templates.get(response_type, self.response_templates['default'])
        base_response = random.choice(templates)
        
        # Enhance with context
        contextual_response = self.generate_contextual_response(base_response, context)
        
        # Add to conversation history
        self.conversation_history.append({
            'user': prompt,
            'assistant': contextual_response
        })
        
        return contextual_response
    
    def add_to_history(self, prompt: str, response: str):
        """Add exchange to conversation history."""
        self.conversation_history.append({
            'user': prompt,
            'assistant': response
        })
    
    def is_available(self) -> bool:
        """Demo AI is always available."""
        return True
    
    def initialize(self) -> bool:
        """Initialize demo AI."""
        return True

class SpectraAIDemo:
    """SpectraAI Demo Mode - Full functionality without external AI providers."""
    
    def __init__(self):
        self.personality = SpectraPersonality()
        self.memory = SpectraMemory()
        self.emotions = EmotionEngine()
        self.reflection = ReflectionEngine()
        self.ai = DemoAI()
        self.conversation_count = 0
        self.is_running = False
    
    def initialize(self):
        """Initialize all demo components."""
        logger.info("🚀 Initializing SpectraAI Demo Mode...")
        
        # Initialize components
        self.memory.initialize()
        self.emotions.initialize()
        
        logger.info("✅ Demo mode initialized successfully!")
        return True
    
    def display_startup_info(self):
        """Display demo startup information."""
        print("\n" + "="*60)
        print("🌟 SpectraAI - DEMO MODE")
        print("="*60)
        print("🆓 Running in FREE demo mode - no API keys required!")
        print("🤖 AI Provider: Local Demo (100% FREE)")
        print("💭 Memory: Active and learning")
        print("😊 Emotions: Active and responsive")
        print("🎭 Personality: Dynamic and adaptive")
        print("="*60)
        print("\n💡 This demo shows all SpectraAI features without external AI!")
        print("   Try asking questions, sharing emotions, or just chatting!")
        print("\nType 'help' for commands, 'quit' to exit")
        print("How can I assist you today?\n")
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input through the demo system."""
        
        # Handle special commands
        if user_input.lower() in ['quit', 'exit', 'bye']:
            return "EXIT_COMMAND"
        
        if user_input.lower() == 'help':
            return self._get_help_text()
        
        if user_input.lower().startswith('/'):
            return self._handle_command(user_input)
        
        # Process through all systems
        try:
            # 1. Store in memory
            self.memory.store_interaction(user_input, "user")
            
            # 2. Analyze emotions
            user_emotions = self.emotions.analyze_text(user_input)
            self.emotions.update_state(user_emotions)
            
            # 3. Get relevant memories
            relevant_memories = self.memory.get_relevant_memories(user_input, limit=3)
            
            # 4. Build context
            context = {
                'personality': self.personality.get_current_state(),
                'emotions': self.emotions.get_emotional_state(),
                'relevant_memories': relevant_memories,
                'user_emotions': user_emotions
            }
            
            # 5. Generate response using demo AI
            response = self.ai.generate_response(user_input, context)
            
            # 6. Store AI response in memory
            self.memory.store_interaction(response, "assistant")
            
            # 7. Update personality based on interaction
            self.personality.update_from_interaction(user_input, response)
            
            # 8. Reflect on conversation periodically
            self.conversation_count += 1
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Error processing input: {e}")
            return "I'm experiencing some technical difficulties in demo mode. Let me try to help you anyway!"
    
    def _get_help_text(self) -> str:
        """Get help text for demo mode."""
        return """
🆘 SpectraAI Demo Mode Commands:
───────────────────────────────
• /status     - Show system status
• /memory     - View recent memories
• /emotions   - Show current emotional state  
• /personality - View personality state
• /clear      - Clear conversation history
• help        - Show this help message
• quit/exit   - Exit SpectraAI Demo

🎭 Demo Features:
• Dynamic personality that adapts to conversation
• Emotional analysis and response adaptation
• Memory system that remembers our conversations
• Self-reflection and learning capabilities
• Contextual responses based on mood and history

💡 This is a FULL demonstration of SpectraAI capabilities!
"""
    
    def _handle_command(self, command: str) -> str:
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
        elif cmd == 'clear':
            return self._clear_conversation()
        else:
            return "❓ Unknown command. Type 'help' for available commands."
    
    def _get_status_info(self) -> str:
        """Get demo system status."""
        return f"""
📊 SpectraAI Demo Status:
────────────────────────
🤖 AI Provider: Local Demo (FREE)
💰 Cost: Completely FREE
🔗 Status: Active and responsive
💭 Memory Count: {self.memory.get_memory_count()}
😊 Emotional State: {len(self.emotions.get_emotional_state())} active emotions
🎭 Current Mood: {self.personality.get_current_state().get('current_mood', 'neutral')}
💬 Conversation Turns: {self.conversation_count}
"""
    
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
    
    def _clear_conversation(self) -> str:
        """Clear conversation history."""
        self.ai.conversation_history.clear()
        self.conversation_count = 0
        return "🧹 Conversation history cleared!"
    
    def run(self):
        """Main demo conversation loop."""
        
        # Initialize
        if not self.initialize():
            print("❌ Failed to initialize demo mode. Exiting.")
            return
        
        # Display startup info
        self.display_startup_info()
        
        # Main conversation loop
        self.is_running = True
        
        try:
            while self.is_running:
                try:
                    # Get user input
                    user_input = input("🔵 You: ").strip()
                    
                    if not user_input:
                        continue
                    
                    # Process input
                    response = self.process_user_input(user_input)
                    
                    # Handle exit command
                    if response == "EXIT_COMMAND":
                        print("🌟 SpectraAI Demo: Thank you for trying the demo! Take care! 👋")
                        break
                    
                    # Display response
                    print(f"🤖 SpectraAI: {response}\n")
                    
                except KeyboardInterrupt:
                    print("\n\n🌟 SpectraAI Demo: Goodbye! Thanks for trying the demo! 👋")
                    break
                    
                except Exception as e:
                    logger.error(f"❌ Error in demo loop: {e}")
                    print("❌ Demo encountered an error. Let me try to continue.\n")
                    continue
        
        finally:
            logger.info("🔚 SpectraAI Demo session ended")

def main():
    """Main entry point for demo mode."""
    try:
        demo = SpectraAIDemo()
        demo.run()
        
    except Exception as e:
        logger.error(f"❌ Demo error: {e}")
        print(f"❌ Demo error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Run the demo
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error starting demo: {e}")
        sys.exit(1)
