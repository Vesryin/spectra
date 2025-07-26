#!/usr/bin/env python3
"""
Quick test for OpenHermes model integration with SpectraAI
"""

import asyncio
import logging

from logic.ai_manager import AIManager

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_openhermes():
    """Test OpenHermes specifically."""
    print("🧠 Testing OpenHermes integration with SpectraAI...")
    print("=" * 60)
    
    # Initialize AI manager
    ai_manager = AIManager()
    
    # Initialize providers
    if await ai_manager.initialize():
        print("✅ AI Manager initialized successfully!")
        print(f"🤖 Active provider: {ai_manager.active_provider.__class__.__name__}")
        
        if hasattr(ai_manager.active_provider, 'model'):
            print(f"📖 Model: {ai_manager.active_provider.model}")
        
        print("\n" + "=" * 60)
        
        # Test questions to see OpenHermes in action
        test_questions = [
            "Hello! What's your name?",
            "Tell me something interesting about artificial intelligence.",
            "What makes you special as an AI companion?"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n💬 Question {i}: {question}")
            print("🤔 Thinking...")
            
            try:
                response = await ai_manager.generate_response(question)
                print(f"🎯 Response: {response}")
                print("-" * 40)
                
            except Exception as e:
                print(f"❌ Error: {e}")
                break
        
        print("\n🎉 OpenHermes test completed!")
        
    else:
        print("❌ Failed to initialize AI Manager")
        print("🔍 Checking what went wrong...")
        
        # Get provider status
        status = await ai_manager.get_provider_status()
        for provider_name, details in status.items():
            print(f"  {provider_name}: {'✅' if details['available'] else '❌'} {details.get('error', '')}")

if __name__ == "__main__":
    asyncio.run(test_openhermes())
