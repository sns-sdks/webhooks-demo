import pytest
from httpx import AsyncClient

from app.main import app


@pytest.fixture
def client():
    return AsyncClient(app=app, base_url="https://test")
