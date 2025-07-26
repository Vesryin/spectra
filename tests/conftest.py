# tests/conftest.py

"""Pytest configuration and fixtures for SpectraAI tests."""

import pytest
import tempfile
from pathlib import Path
import os

@pytest.fixture
def temp_memory_file():
    """Create a temporary memory file for testing."""
    temp_dir = Path(tempfile.mkdtemp())
    memory_file = temp_dir / "test_memory.json"
    yield memory_file
    
    # Cleanup
    if memory_file.exists():
        memory_file.unlink()
    temp_dir.rmdir()

@pytest.fixture
def mock_openai_key(monkeypatch):
    """Mock OpenAI API key for testing."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-123")

@pytest.fixture
def test_config():
    """Test configuration values."""
    return {
        "test_mode": True,
        "memory_limit": 10,
        "debug": True
    }
