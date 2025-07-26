"""
Test configuration for SpectraAI API
Modern pytest setup with async support and comprehensive fixtures
"""

import asyncio
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    # Import your FastAPI app here when created
    # from app.main import app
    # return TestClient(app)
    pass


@pytest.fixture
async def async_client():
    """Create an async test client for the FastAPI application."""
    # Import your FastAPI app here when created
    # from app.main import app
    # async with AsyncClient(app=app, base_url="http://test") as ac:
    #     yield ac
    pass


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API responses for testing."""
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "This is a test response from SpectraAI."
                }
            }
        ],
        "usage": {"total_tokens": 25}
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "id": "test_user_123",
        "email": "test@spectraai.com",
        "name": "Test User",
        "preferences": {
            "theme": "dark",
            "language": "en"
        }
    }
