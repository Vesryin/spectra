# test_ai_system.py

"""
SpectraAI System Test - Test all AI providers and components
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from logic.ai_manager import get_ai_manager
from logic.brain import get_brain
from core.personality import SpectraPersonality
from core.memory import SpectraMemory
from core.emotions import EmotionEngine
from config.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SystemTester:
    """Test all SpectraAI components."""
    
    def __init__(self):
        self.test_results = {}
        self.overall_success = True
    
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Log test result."""
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} {test_name}: {message}")
        self.test_results[test_name] = {"success": success, "message": message}
        if not success:
            self.overall_success = False
    
    async def test_ai_manager(self):
        """Test AI Manager initialization and provider detection."""
        logger.info("\n🤖 Testing AI Manager...")
        
        try:
            ai_manager = get_ai_manager()
            await ai_manager.initialize()
            
            self.log_test("AI Manager Init", True, "Initialized successfully")
            
            # Test provider info
            active_provider = ai_manager.get_active_provider_info()
            provider_name = active_provider.get('name', 'unknown')
            is_free = active_provider.get('is_free', False)
            
            self.log_test("Active Provider", True, f"{provider_name} ({'FREE' if is_free else 'PAID'})")
            
            # Test all providers status
            all_providers = ai_manager.get_all_providers_status()
            available_count = sum(1 for p in all_providers.values() if p.get('available'))
            
            self.log_test("Provider Discovery", True, f"{available_count} providers available")
            
            return ai_manager
            
        except Exception as e:
            self.log_test("AI Manager Init", False, str(e))
            return None
    
    async def test_brain(self):
        """Test Brain initialization and thinking."""
        logger.info("\n🧠 Testing Brain...")
        
        try:
            brain = get_brain()
            await brain.initialize()
            
            self.log_test("Brain Init", True, "Initialized successfully")
            
            # Test thinking
            test_prompt = "Hello, this is a test message."
            response = await brain.think(test_prompt)
            
            if response and len(response) > 10:
                self.log_test("Brain Thinking", True, f"Response: {response[:50]}...")
            else:
                self.log_test("Brain Thinking", False, "Response too short or empty")
            
            # Test provider status
            status = brain.get_provider_status()
            self.log_test("Brain Status", True, f"Active provider: {status.get('active_provider', {}).get('name', 'unknown')}")
            
            return brain
            
        except Exception as e:
            self.log_test("Brain Init", False, str(e))
            return None
    
    def test_personality(self):
        """Test Personality system."""
        logger.info("\n🎭 Testing Personality...")
        
        try:
            personality = SpectraPersonality()
            
            # Test current state
            state = personality.get_current_state()
            mood = state.get('current_mood', 'unknown')
            
            self.log_test("Personality Init", True, f"Current mood: {mood}")
            
            # Test mood change
            personality.update_mood('happy', 0.7)
            new_state = personality.get_current_state()
            new_mood = new_state.get('current_mood', 'unknown')
            
            self.log_test("Mood Update", True, f"New mood: {new_mood}")
            
            return personality
            
        except Exception as e:
            self.log_test("Personality Init", False, str(e))
            return None
    
    def test_memory(self):
        """Test Memory system."""
        logger.info("\n💭 Testing Memory...")
        
        try:
            memory = SpectraMemory()
            memory.initialize()
            
            # Test storing interaction
            memory.store_interaction("Test message", "user")
            memory.store_interaction("Test response", "assistant")
            
            count = memory.get_memory_count()
            self.log_test("Memory Storage", count >= 2, f"Stored {count} memories")
            
            # Test retrieval
            recent = memory.get_recent_memories(2)
            self.log_test("Memory Retrieval", len(recent) >= 2, f"Retrieved {len(recent)} memories")
            
            # Test search
            relevant = memory.get_relevant_memories("test", limit=1)
            self.log_test("Memory Search", len(relevant) >= 1, f"Found {len(relevant)} relevant memories")
            
            return memory
            
        except Exception as e:
            self.log_test("Memory Init", False, str(e))
            return None
    
    def test_emotions(self):
        """Test Emotions system."""
        logger.info("\n😊 Testing Emotions...")
        
        try:
            emotions = EmotionEngine()
            emotions.initialize()
            
            # Test emotion analysis
            happy_text = "I'm so happy and excited!"
            emotions_detected = emotions.analyze_text(happy_text)
            
            self.log_test("Emotion Analysis", len(emotions_detected) > 0, f"Detected {len(emotions_detected)} emotions")
            
            # Test emotion update
            emotions.update_state(emotions_detected)
            current_state = emotions.get_emotional_state()
            
            self.log_test("Emotion State", len(current_state) > 0, f"Current state: {len(current_state)} emotions")
            
            return emotions
            
        except Exception as e:
            self.log_test("Emotions Init", False, str(e))
            return None
    
    async def test_integration(self, brain, personality, memory, emotions):
        """Test integration between all components."""
        logger.info("\n🔗 Testing Integration...")
        
        try:
            # Test full pipeline
            user_input = "Tell me a joke about programming"
            
            # Store in memory
            memory.store_interaction(user_input, "user")
            
            # Analyze emotions
            user_emotions = emotions.analyze_text(user_input)
            emotions.update_state(user_emotions)
            
            # Get relevant memories
            relevant_memories = memory.get_relevant_memories(user_input, limit=2)
            
            # Build context
            context = {
                'personality': personality.get_current_state(),
                'emotions': emotions.get_emotional_state(),
                'relevant_memories': relevant_memories,
                'user_emotions': user_emotions
            }
            
            # Generate response
            response = await brain.think(user_input, context)
            
            # Store response
            memory.store_interaction(response, "assistant")
            
            # Update personality
            personality.update_from_interaction(user_input, response)
            
            if response and len(response) > 20:
                self.log_test("Full Integration", True, f"Generated contextual response: {response[:50]}...")
            else:
                self.log_test("Full Integration", False, "Integration failed")
            
        except Exception as e:
            self.log_test("Full Integration", False, str(e))
    
    def test_configuration(self):
        """Test configuration loading."""
        logger.info("\n⚙️ Testing Configuration...")
        
        try:
            # Test settings access
            ai_provider = getattr(settings, 'AI_PROVIDER', 'local')
            max_tokens = getattr(settings, 'MAX_TOKENS', 300)
            
            self.log_test("Config Loading", True, f"AI Provider: {ai_provider}, Max Tokens: {max_tokens}")
            
            # Test environment variables
            import os
            
            # Note: Environment variables loaded automatically by settings module
            
            # Check if .env file exists
            env_file = Path('.env')
            if env_file.exists():
                self.log_test("Environment File", True, ".env file found")
            else:
                self.log_test("Environment File", False, ".env file not found (using defaults)")
            
        except Exception as e:
            self.log_test("Config Loading", False, str(e))
    
    async def run_all_tests(self):
        """Run all system tests."""
        logger.info("🧪 Starting SpectraAI System Tests")
        logger.info("="*50)
        
        # Test configuration first
        self.test_configuration()
        
        # Test AI components
        await self.test_ai_manager()
        brain = await self.test_brain()
        
        # Test core components
        personality = self.test_personality()
        memory = self.test_memory()
        emotions = self.test_emotions()
        
        # Test integration if all components loaded
        if all([brain, personality, memory, emotions]):
            await self.test_integration(brain, personality, memory, emotions)
        else:
            self.log_test("Integration Test", False, "Some components failed to load")
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary."""
        logger.info("\n" + "="*50)
        logger.info("🧪 Test Summary")
        logger.info("="*50)
        
        passed = sum(1 for result in self.test_results.values() if result['success'])
        total = len(self.test_results)
        
        for test_name, result in self.test_results.items():
            status = "✅" if result['success'] else "❌"
            logger.info(f"{status} {test_name}: {result['message']}")
        
        logger.info(f"\n📊 Results: {passed}/{total} tests passed")
        
        if self.overall_success:
            logger.info("🎉 All tests passed! SpectraAI is ready to use!")
        else:
            logger.info("⚠️ Some tests failed. Check the logs above.")
        
        return self.overall_success

async def main():
    """Run the system tests."""
    try:
        tester = SystemTester()
        success = await tester.run_all_tests()
        
        if success:
            print("\n🚀 Ready to start SpectraAI! Run: python main.py")
            sys.exit(0)
        else:
            print("\n❌ Some issues detected. Please check the logs.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n❌ Tests cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Test runner failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
