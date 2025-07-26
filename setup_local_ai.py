# setup_local_ai.py

"""
SpectraAI Local AI Setup Script
Automatically installs and configures free local AI providers
"""

import subprocess
import sys
import os
import platform
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class LocalAISetup:
    """Setup class for installing local AI providers."""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.arch = platform.machine().lower()
        self.project_root = Path(__file__).parent
    
    def run_command(self, command: str, check: bool = True) -> subprocess.CompletedProcess:
        """Run a shell command."""
        logger.info(f"Running: {command}")
        return subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
    
    def install_python_packages(self):
        """Install required Python packages."""
        logger.info("📦 Installing Python packages...")
        
        # Install core packages
        packages = [
            "transformers>=4.35.0",
            "torch>=2.0.0",
            "httpx>=0.25.0",
            "aiofiles>=23.0.0",
            "pydantic>=2.5.0"
        ]
        
        for package in packages:
            try:
                self.run_command(f"{sys.executable} -m pip install {package}")
                logger.info(f"✅ Installed {package}")
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ Failed to install {package}: {e}")
                logger.error(f"Output: {e.stdout}")
                logger.error(f"Error: {e.stderr}")
    
    def check_ollama_installed(self) -> bool:
        """Check if Ollama is installed."""
        try:
            result = self.run_command("ollama --version", check=False)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def install_ollama(self):
        """Install Ollama for local Llama models."""
        logger.info("🦙 Installing Ollama for local Llama models...")
        
        if self.check_ollama_installed():
            logger.info("✅ Ollama is already installed")
            return True
        
        try:
            if self.system == "windows":
                logger.info("Please download and install Ollama from: https://ollama.ai/download/windows")
                logger.info("After installation, run: ollama pull openhermes")
                return False
            
            elif self.system == "darwin":  # macOS
                # Download and install Ollama for macOS
                logger.info("Installing Ollama for macOS...")
                self.run_command("curl -fsSL https://ollama.ai/install.sh | sh")
            
            elif self.system == "linux":
                # Install Ollama for Linux
                logger.info("Installing Ollama for Linux...")
                self.run_command("curl -fsSL https://ollama.ai/install.sh | sh")
            
            else:
                logger.error(f"Unsupported system: {self.system}")
                return False
            
            logger.info("✅ Ollama installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install Ollama: {e}")
            return False
    
    def pull_ollama_models(self):
        """Pull essential Ollama models."""
        if not self.check_ollama_installed():
            logger.error("❌ Ollama not installed. Please install it first.")
            return False
        
        models = [
            "openhermes",       # OpenHermes 2.5 - Best conversation model (RECOMMENDED)
            "llama3.2:3b",      # LLaMA 3.2 3B - Modern, fast alternative 
            "mistral"           # Mistral 7B - Alternative model
        ]
        
        logger.info("📥 Pulling Ollama models...")
        
        for model in models:
            try:
                logger.info(f"Pulling {model} (this may take a while)...")
                self.run_command(f"ollama pull {model}")
                logger.info(f"✅ {model} ready")
            except subprocess.CalledProcessError as e:
                logger.warning(f"⚠️ Failed to pull {model}: {e}")
                continue
        
        return True
    
    def test_huggingface_models(self):
        """Test Hugging Face models installation."""
        logger.info("🤗 Testing Hugging Face models...")
        
        test_script = '''
import os
os.environ["TRANSFORMERS_CACHE"] = "./models_cache"

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    import torch
    
    print("✅ Transformers library loaded successfully")
    
    # Test a small model
    model_name = "microsoft/DialoGPT-small"
    print(f"📥 Loading {model_name}...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    print("✅ Model loaded successfully")
    
    # Test generation
    generator = pipeline("text-generation", 
                        model=model, 
                        tokenizer=tokenizer,
                        device=0 if torch.cuda.is_available() else -1)
    
    result = generator("Hello, how are you?", max_length=50, num_return_sequences=1)
    print(f"✅ Test generation: {result[0]['generated_text']}")
    
    print("🎉 Hugging Face models are working!")
    
except Exception as e:
    print(f"❌ Error testing Hugging Face: {e}")
    import traceback
    traceback.print_exc()
'''
        
        try:
            # Write test script to temporary file
            test_file = self.project_root / "test_hf.py"
            test_file.write_text(test_script)
            
            # Run test
            self.run_command(f"{sys.executable} {test_file}")
            logger.info("✅ Hugging Face models test completed")
            
            # Cleanup
            test_file.unlink()
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Hugging Face test failed: {e}")
            logger.error(f"Output: {e.stdout}")
            logger.error(f"Error: {e.stderr}")
            return False
    
    def create_example_configs(self):
        """Create example configuration files."""
        logger.info("⚙️ Creating example configuration files...")
        
        # Create .env.example file
        env_example = '''# SpectraAI Configuration
# Copy this file to .env and configure your settings

# AI Provider Selection (uncomment one)
AI_PROVIDER=local
# AI_PROVIDER=huggingface
# AI_PROVIDER=ollama
# AI_PROVIDER=openai

# OpenAI Configuration (for paid API)
# OPENAI_API_KEY=your_openai_api_key_here
# OPENAI_MODEL=gpt-3.5-turbo

# Ollama Configuration (for local Llama models)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=openhermes

# Hugging Face Configuration (for free local models)
HUGGINGFACE_MODEL=microsoft/DialoGPT-small

# General AI Settings
MAX_TOKENS=300
TEMPERATURE=0.8
MAX_CONTEXT_LENGTH=10

# System Settings
LOG_LEVEL=INFO
'''
        
        env_file = self.project_root / ".env.example"
        env_file.write_text(env_example)
        logger.info(f"✅ Created {env_file}")
        
        # Create startup script
        if self.system == "windows":
            startup_script = '''@echo off
echo Starting SpectraAI with Local AI...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\\Scripts\\activate

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Start SpectraAI
echo Starting SpectraAI...
python main.py

pause
'''
            script_file = self.project_root / "start_spectra.bat"
            script_file.write_text(startup_script)
            logger.info(f"✅ Created {script_file}")
        
        else:  # Unix-like systems
            startup_script = '''#!/bin/bash
echo "Starting SpectraAI with Local AI..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Start SpectraAI
echo "Starting SpectraAI..."
python main.py
'''
            script_file = self.project_root / "start_spectra.sh"
            script_file.write_text(startup_script)
            script_file.chmod(0o755)  # Make executable
            logger.info(f"✅ Created {script_file}")
    
    def run_setup(self):
        """Run the complete setup process."""
        logger.info("🚀 Starting SpectraAI Local AI Setup...")
        logger.info("="*50)
        
        # 1. Install Python packages
        self.install_python_packages()
        
        # 2. Install Ollama (optional)
        logger.info("\n🦙 Ollama Setup (for Llama models):")
        if not self.install_ollama():
            logger.info("⚠️ Ollama installation skipped. You can install it manually later.")
        else:
            # Pull models if Ollama is installed
            self.pull_ollama_models()
        
        # 3. Test Hugging Face
        logger.info("\n🤗 Testing Hugging Face Models:")
        self.test_huggingface_models()
        
        # 4. Create configuration files
        logger.info("\n⚙️ Creating Configuration Files:")
        self.create_example_configs()
        
        # 5. Final instructions
        logger.info("\n" + "="*50)
        logger.info("🎉 Local AI Setup Complete!")
        logger.info("="*50)
        logger.info("\nNext steps:")
        logger.info("1. Copy .env.example to .env and configure your settings")
        logger.info("2. Set AI_PROVIDER=local in your .env file for free local AI")
        logger.info("3. Run python main.py or use the start script")
        logger.info("\nFor Ollama models:")
        logger.info("- Make sure Ollama service is running: ollama serve")
        logger.info("- Set AI_PROVIDER=ollama in your .env file")
        logger.info("\nFor Hugging Face models:")
        logger.info("- Set AI_PROVIDER=huggingface in your .env file")
        logger.info("\n💡 All providers are FREE and run locally!")

def main():
    """Main setup function."""
    try:
        setup = LocalAISetup()
        setup.run_setup()
    except KeyboardInterrupt:
        print("\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
