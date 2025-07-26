# launch.py

"""Easy launch script for SpectraAI with setup validation."""

import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = ['openai', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def check_api_key():
    """Check if OpenAI API key is configured."""
    try:
        from config.settings import settings
        return bool(settings.OPENAI_API_KEY)
    except:
        return False

def setup_environment():
    """Set up the environment with user guidance."""
    print("🔧 Setting up SpectraAI...")
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print("✅ Dependencies installed!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run: pip install -r requirements.txt")
            return False
    
    # Check API key
    if not check_api_key():
        print("\n🔑 OpenAI API Key Setup Required")
        print("Please follow these steps:")
        print("1. Get your API key from: https://platform.openai.com/api-keys")
        print("2. Edit the file: config/secrets.env")
        print("3. Set: OPENAI_API_KEY=your_actual_api_key_here")
        print("4. Save the file and run this script again")
        return False
    
    return True

def run_tests():
    """Run basic tests."""
    print("\n🧪 Running basic tests...")
    try:
        import test_runner
        success = test_runner.run_basic_tests()
        return success
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main launch function."""
    print("🌟 SpectraAI Launcher")
    print("="*40)
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Setup incomplete. Please fix the issues above and try again.")
        return
    
    # Run tests
    if not run_tests():
        print("\n⚠️  Some tests failed, but you can still try running SpectraAI.")
        response = input("Continue anyway? (y/n): ").lower()
        if response != 'y':
            return
    
    # Launch SpectraAI
    print("\n🚀 Launching SpectraAI...")
    print("="*40)
    
    try:
        from main import main as spectra_main
        spectra_main()
    except KeyboardInterrupt:
        print("\n\n👋 SpectraAI session ended.")
    except Exception as e:
        print(f"\n❌ Error running SpectraAI: {e}")
        print("Try running: python test_runner.py --api")

if __name__ == "__main__":
    main()
