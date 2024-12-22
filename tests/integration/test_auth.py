import os
from fastapi.testclient import TestClient
from app.api.main import app
from dotenv import load_dotenv

load_dotenv(".env")
client = TestClient(app)


def test_user_authenticate_success():
    response = client.post(
        "/token",
        json={
            "username": os.getenv("USER_USERNAME"),
            "password": os.getenv("USER_PASSWORD"),
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json().get("token_type") == "bearer"


def test_admin_authenticate_success():
    response = client.post(
        "/token",
        json={
            "username": os.getenv("ADMIN_USERNAME"),
            "password": os.getenv("ADMIN_PASSWORD"),
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json().get("token_type") == "bearer"


def test_authenticate_invalid_user():
    response = client.post(
        "/token", json={"username": "invalid_user", "password": "wrong_password"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid credentials"}


def test_authenticate_invalid_password():
    response = client.post(
        "/token",
        json={"username": os.getenv("USER_USERNAME"), "password": "wrong_password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid credentials"}


def test_missing_endpoint():
    response = client.post(
        "/nonexistent",
        json={
            "username": os.getenv("ADMIN_USERNAME"),
            "password": os.getenv("ADMIN_PASSWORD"),
        },
    )

    assert response.status_code == 404
