"""
SpectraAI Configuration Management
Environment-based configuration with validation and type safety.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, List

from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application settings
    DEBUG: bool = Field(default=False, env="DEBUG")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    HOST: str = Field(default="127.0.0.1", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    # Security settings
    SECRET_KEY: str = Field(default="your-secret-key-here", env="SECRET_KEY")
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        env="ALLOWED_ORIGINS"
    )
    ALLOWED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1", "*"],
        env="ALLOWED_HOSTS"
    )
    
    # Database settings
    DATABASE_URL: str = Field(
        default="postgresql://username:password@localhost:5432/spectra_db",
        env="DATABASE_URL"
    )
    
    # AI Provider settings
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4", env="OPENAI_MODEL")
    OPENHERMES_BASE_URL: str = Field(
        default="http://localhost:11434", 
        env="OPENHERMES_BASE_URL"
    )
    
    # Redis settings (for caching and sessions)
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    # Logging settings
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("ALLOWED_HOSTS", pre=True)
    def parse_allowed_hosts(cls, v):
        """Parse allowed hosts from string or list."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    @validator("OPENAI_API_KEY")
    def validate_openai_key(cls, v):
        """Validate OpenAI API key format."""
        if v and not v.startswith(("sk-", "your-")):
            raise ValueError("Invalid OpenAI API key format")
        return v
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


# Environment-specific configurations
def get_database_url() -> str:
    """Get database URL with environment-specific defaults."""
    settings = get_settings()
    
    if settings.ENVIRONMENT == "test":
        return settings.DATABASE_URL.replace("spectra_db", "spectra_test_db")
    elif settings.ENVIRONMENT == "production":
        # Production database should be explicitly set
        if "localhost" in settings.DATABASE_URL:
            raise ValueError("Production database URL cannot use localhost")
    
    return settings.DATABASE_URL


def is_development() -> bool:
    """Check if running in development mode."""
    return get_settings().DEBUG or get_settings().ENVIRONMENT == "development"


def is_production() -> bool:
    """Check if running in production mode."""
    return get_settings().ENVIRONMENT == "production"
