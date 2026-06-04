import pytest
from fastapi.testclient import TestClient
import os

# Set required env vars BEFORE importing the app.
# This prevents Settings validation from failing during tests.
os.environ.setdefault("GROQ_API_KEY", "test_groq_key_for_testing")
os.environ.setdefault("ENVIRONMENT", "testing")
os.environ.setdefault("LOG_LEVEL", "WARNING")

from main import app


@pytest.fixture(scope="module")
def client():
    """Provides a FastAPI TestClient for integration tests."""
    with TestClient(app) as c:
        yield c
