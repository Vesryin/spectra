# config/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent / "secrets.env")

class Settings:
    """Application settings and configuration."""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Application Settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # File Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    MEMORY_FILE = DATA_DIR / "memory_store.json"
    
    # Conversation Settings
    MAX_MEMORY_CONTEXT = 5
    MAX_TOKENS = 300
    TEMPERATURE = 0.8
    
    # Personality Traits (0.0 to 1.0)
    PERSONALITY_TRAITS = {
        "empathy": 0.9,
        "creativity": 0.95,
        "humor": 0.7,
        "curiosity": 0.85,
        "warmth": 0.88,
        "patience": 0.9,
        "wisdom": 0.8
    }
    
    @classmethod
    def validate(cls):
        """Validate required settings."""
        errors = []
        
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required")
        
        if not cls.DATA_DIR.exists():
            cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
            
        return errors

# Global settings instance
settings = Settings()
