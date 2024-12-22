import pytest
from fastapi.testclient import TestClient
from httpx import Response, RequestError
import respx
from app.api.main import app, FAKE_API_TOKEN_ENDPOINT

client = TestClient(app)


valid_credentials = {"username": "testuser", "password": "password123"}
invalid_credentials = {"username": "wronguser", "password": "wrongpass"}


@pytest.mark.parametrize(
    "credentials, mock_response_status, mock_response_body, expected_status_code, expected_response_body",
    [
        # Test case: Successful authentication
        (
            valid_credentials,
            200,
            {"access_token": "fake_token", "token_type": "bearer"},
            200,
            {"access_token": "fake_token", "token_type": "bearer"},
        ),
        # Test case: Invalid credentials
        (
            invalid_credentials,
            401,
            {"detail": "Unauthorized"},
            400,
            {"detail": "Invalid credentials"},
        ),
        # Test case: Server error
        (
            valid_credentials,
            500,
            {"detail": "Internal Server Error"},
            400,
            {"detail": "Invalid credentials"},
        ),
    ],
)
@respx.mock
def test_authenticate(
    respx_mock,
    credentials,
    mock_response_status,
    mock_response_body,
    expected_status_code,
    expected_response_body,
):
    respx_mock.post(FAKE_API_TOKEN_ENDPOINT).mock(
        return_value=Response(mock_response_status, json=mock_response_body)
    )

    response = client.post("/token", json=credentials)

    assert response.status_code == expected_status_code
    assert response.json() == expected_response_body


@pytest.mark.parametrize(
    "request_body, expected_status_code",
    [
        ({"password": "password123"}, 422),  # Missing username
        ({"username": "testuser"}, 422),  # Missing password
        ({}, 422),  # Empty body
        (["this_is_not_a_dict"], 422),  # Invalid body format (list instead of dict)
    ],
)
def test_authenticate_validation_errors(request_body, expected_status_code):
    response = client.post("/token", json=request_body)

    assert response.status_code == expected_status_code
