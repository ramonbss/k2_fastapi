import pytest
from unittest.mock import AsyncMock, patch

SERVICE_PATH = "app.api.services.service"


@pytest.fixture
def mock_httpx_client():
    """Fixture to patch httpx.AsyncClient"""

    with patch(f"{SERVICE_PATH}.httpx.AsyncClient") as mock_client:
        yield mock_client


@pytest.fixture
def mock_check_role():
    """Fixture to patch check_role"""
    with patch(f"{SERVICE_PATH}.check_role") as mock_check_role:
        yield mock_check_role


@pytest.fixture
def mock_reset_access_token():
    """Fixture to patch reset_access_token"""
    with patch(f"{SERVICE_PATH}.reset_access_token") as mock_reset_access_token:
        yield mock_reset_access_token
