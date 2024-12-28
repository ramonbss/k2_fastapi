import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from app.api.database import User
from app.api.services.service import get_user_informations, get_access_token
from app.core.config import REMOTE_TOKEN_URL, ROLE_USER

SERVICE_PATH = "app.api.services"


@pytest.mark.asyncio
async def test_get_user_informations_success(
    mock_reset_access_token, mock_check_role, mock_httpx_client
):
    # Mock role checking
    mock_check_role.return_value = None

    # Mock HTTP response from the external endpoint
    mock_response = AsyncMock(status_code=200, json=lambda: {"data": "user_data"})
    mock_httpx_client.return_value.__aenter__.return_value.get.return_value = (
        mock_response
    )

    token = "Bearer test_token"
    result = await get_user_informations(ROLE_USER, token, "http://example.com/user")

    assert result == {"data": "user_data"}
    mock_check_role.assert_called_once_with(ROLE_USER, "test_token")
    mock_httpx_client.return_value.__aenter__.return_value.get.assert_called_once_with(
        "http://example.com/user", headers={"Authorization": token}
    )
    mock_reset_access_token.assert_not_called()


@pytest.mark.asyncio
async def test_get_user_informations_unauthorized(
    mock_reset_access_token, mock_check_role, mock_httpx_client
):
    mock_check_role.return_value = None

    mock_response = AsyncMock(
        status_code=401,
    )
    mock_httpx_client.return_value.__aenter__.return_value.get.return_value = (
        mock_response
    )

    token = "Bearer test_token"
    with pytest.raises(HTTPException) as exc_info:
        await get_user_informations(ROLE_USER, token, "http://example.com/user")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Error while authenticating, try again"
    mock_reset_access_token.assert_called_once_with("test_token", User)
    mock_check_role.assert_called_once_with(ROLE_USER, "test_token")


@pytest.mark.asyncio
async def test_get_user_informations_other_error(mock_check_role, mock_httpx_client):
    mock_check_role.return_value = None

    mock_response = AsyncMock(
        status_code=500, json=lambda: {"error": "Internal Server Error"}
    )
    mock_httpx_client.return_value.__aenter__.return_value.get.return_value = (
        mock_response
    )

    token = "Bearer test_token"
    with pytest.raises(HTTPException) as exc_info:
        await get_user_informations(ROLE_USER, token, "http://example.com/user")

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == {"error": "Internal Server Error"}


@pytest.mark.asyncio
@patch(f"{SERVICE_PATH}.service.create_or_update_user")
async def test_get_access_token_success(mock_create_or_update_user, mock_httpx_client):
    # Mock HTTP response from the token endpoint
    mock_response = AsyncMock(
        json=lambda: {"access_token": "test_access_token"}, status_code=200
    )
    mock_httpx_client.return_value.__aenter__.return_value.post.return_value = (
        mock_response
    )

    # Call the function with mocked dependencies
    username = "testuser"
    password = "testpassword"
    role = ROLE_USER

    result = await get_access_token(username, password, role)

    # Assertions
    assert result == "test_access_token"

    mock_create_or_update_user.assert_called_once_with(
        username="testuser", role=ROLE_USER, token="test_access_token"
    )
    mock_httpx_client.return_value.__aenter__.return_value.post.assert_called_once_with(
        REMOTE_TOKEN_URL,
        params={"username": username, "role": role, "password": password},
    )


@pytest.mark.asyncio
async def test_get_access_token_failure(mock_httpx_client):
    # Mock HTTP response with a non-200 status code (e.g., 400 Bad Request)
    mock_response = AsyncMock(
        status_code=400, json=lambda: {"error": "Invalid credentials"}
    )
    mock_httpx_client.return_value.__aenter__.return_value.post.return_value = (
        mock_response
    )

    # Call the function and expect an HTTPException
    username = "testuser"
    password = "wrongpassword"
    role = ROLE_USER

    with pytest.raises(HTTPException) as exc_info:
        await get_access_token(username, password, role)

    # Assertions
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == {"error": "Invalid credentials"}
    mock_httpx_client.return_value.__aenter__.return_value.post.assert_called_once_with(
        REMOTE_TOKEN_URL,
        params={"username": username, "role": role, "password": password},
    )
