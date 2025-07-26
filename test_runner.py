# test_runner.py

"""Simple test runner for SpectraAI when pytest is not available."""

import sys
import traceback
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def run_basic_tests():
    """Run basic functionality tests without pytest."""
    
    print("🧪 Running SpectraAI Basic Tests")
    print("="*50)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Settings Configuration
    try:
        from config.settings import settings
        print("✅ Settings import - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Settings import - FAILED: {e}")
        tests_failed += 1
    
    # Test 2: Personality Module
    try:
        from core.personality import SpectraPersonality
        personality = SpectraPersonality()
        assert personality.name == "Spectra"
        assert len(personality.traits) > 0
        description = personality.describe()
        assert "Spectra" in description
        print("✅ Personality module - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Personality module - FAILED: {e}")
        tests_failed += 1
    
    # Test 3: Memory Module
    try:
        from core.memory import SpectraMemory, MemoryEntry
        
        # Test MemoryEntry
        entry = MemoryEntry("Test content", "conversation", 0.8, ["test"])
        assert entry.content == "Test content"
        
        # Test serialization
        data = entry.to_dict()
        new_entry = MemoryEntry.from_dict(data)
        assert new_entry.content == entry.content
        
        # Test SpectraMemory with temporary file
        import tempfile
        temp_file = Path(tempfile.mktemp(suffix=".json"))
        memory = SpectraMemory(temp_file)
        
        # Test basic operations
        memory.remember("Test memory")
        memories = memory.recall()
        assert len(memories) == 1
        assert "Test memory" in memories[0]
        
        # Cleanup
        if temp_file.exists():
            temp_file.unlink()
            
        print("✅ Memory module - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Memory module - FAILED: {e}")
        tests_failed += 1
    
    # Test 4: Emotions Module
    try:
        from core.emotions import EmotionalState, EmotionEngine
        
        # Test EmotionalState
        state = EmotionalState()
        assert len(state.emotions) > 0
        assert "joy" in state.emotions
        
        original_joy = state.emotions["joy"]
        state.update_emotion("joy", 0.1, "test")
        assert state.emotions["joy"] > original_joy
        
        # Test EmotionEngine
        engine = EmotionEngine()
        result = engine.process_input("I'm happy!")
        assert "emotional_response" in result
        assert "tone" in result
        
        print("✅ Emotions module - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Emotions module - FAILED: {e}")
        tests_failed += 1
    
    # Test 5: Reflection Module
    try:
        from core.reflection import ReflectionEngine
        
        reflection = ReflectionEngine()
        assert len(reflection.reflection_prompts) > 0
        
        # Test reflection generation
        test_conversation = ["Hello", "How are you?", "I'm doing well"]
        result = reflection.reflect(test_conversation)
        assert "prompt" in result
        assert "content" in result
        
        print("✅ Reflection module - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Reflection module - FAILED: {e}")
        tests_failed += 1
    
    # Test 6: Brain Module (without API call)
    try:
        from logic.brain import SpectraBrain
        
        # This will fail without API key, but we can test initialization
        try:
            brain = SpectraBrain()
            print("✅ Brain module initialization - PASSED")
            tests_passed += 1
        except ValueError as ve:
            if "API key" in str(ve):
                print("⚠️  Brain module - SKIPPED (No API key configured)")
            else:
                print(f"❌ Brain module - FAILED: {ve}")
                tests_failed += 1
        except Exception as e:
            print(f"❌ Brain module - FAILED: {e}")
            tests_failed += 1
    except Exception as e:
        print(f"❌ Brain module import - FAILED: {e}")
        tests_failed += 1
    
    # Test 7: Main Application (import only)
    try:
        from main import SpectraAI
        print("✅ Main application import - PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Main application import - FAILED: {e}")
        print(f"   Error details: {traceback.format_exc()}")
        tests_failed += 1
    
    # Summary
    print("\n" + "="*50)
    print(f"📊 Test Results:")
    print(f"   ✅ Passed: {tests_passed}")
    print(f"   ❌ Failed: {tests_failed}")
    print(f"   📈 Success Rate: {tests_passed/(tests_passed+tests_failed)*100:.1f}%")
    
    if tests_failed == 0:
        print("\n🎉 All basic tests passed! SpectraAI is ready to run.")
        return True
    else:
        print(f"\n⚠️  {tests_failed} test(s) failed. Please check the errors above.")
        return False

def test_api_integration():
    """Test API integration if key is available."""
    print("\n🔌 Testing API Integration")
    print("-"*30)
    
    try:
        from config.settings import settings
        
        if not settings.OPENAI_API_KEY:
            print("⚠️  No OpenAI API key configured - skipping API tests")
            print("   To test API integration, set OPENAI_API_KEY in config/secrets.env")
            return False
        
        from logic.brain import SpectraBrain
        brain = SpectraBrain()
        
        # Test with a simple query
        print("Testing AI response generation...")
        response = brain.query_spectra("Hello, this is a test message.")
        
        if response and len(response) > 0:
            print("✅ API integration - PASSED")
            print(f"   Sample response: {response[:100]}...")
            return True
        else:
            print("❌ API integration - FAILED: Empty response")
            return False
            
    except Exception as e:
        print(f"❌ API integration - FAILED: {e}")
        return False

if __name__ == "__main__":
    print("🌟 SpectraAI Test Suite")
    print("This will test the basic functionality of all modules.\n")
    
    # Run basic tests
    basic_success = run_basic_tests()
    
    # Test API integration if requested
    if len(sys.argv) > 1 and sys.argv[1] == "--api":
        api_success = test_api_integration()
    else:
        print("\n💡 To test API integration, run: python test_runner.py --api")
        print("   (Make sure to set your OPENAI_API_KEY in config/secrets.env first)")
    
    # Exit with appropriate code
    sys.exit(0 if basic_success else 1)
