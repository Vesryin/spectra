# simple_demo.py

"""
Simple SpectraAI Demo - Quick test of the working AI system
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from logic.brain import get_brain

async def main():
    """Simple demo of the AI system."""
    print("🌟 SpectraAI - Simple Demo")
    print("="*40)
    print("🤖 Testing FREE local AI system...")
    print()
    
    # Initialize brain
    brain = get_brain()
    await brain.initialize()
    
    # Show provider status
    status = brain.get_provider_status()
    active_provider = status.get('active_provider', {})
    provider_name = active_provider.get('name', 'unknown')
    is_free = active_provider.get('is_free', False)
    
    print(f"✅ AI Provider: {provider_name.upper()} ({'FREE' if is_free else 'PAID'})")
    print("💡 Ready to chat! Type 'quit' to exit.")
    print()
    
    # Simple conversation loop
    while True:
        try:
            # Get user input
            user_input = await asyncio.to_thread(input, "You: ")
            user_input = user_input.strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("🌟 SpectraAI: Goodbye! Thanks for chatting! 👋")
                break
            
            # Generate response
            response = await brain.think(user_input)
            print(f"🤖 SpectraAI: {response}")
            print()
            
        except KeyboardInterrupt:
            print("\n🌟 SpectraAI: Goodbye! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
