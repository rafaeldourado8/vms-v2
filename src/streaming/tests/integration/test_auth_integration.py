"""Integration tests for protected endpoints"""
import pytest
from fastapi.testclient import TestClient
from src.streaming.infrastructure.web.main import app

client = TestClient(app)


def test_protected_endpoint_without_token():
    """Test accessing protected endpoint without token"""
    response = client.post("/api/streams/start", json={
        "camera_id": "123e4567-e89b-12d3-a456-426614174000",
        "source_url": "rtsp://test"
    })
    assert response.status_code == 403


def test_protected_endpoint_with_invalid_token():
    """Test accessing protected endpoint with invalid token"""
    response = client.post(
        "/api/streams/start",
        json={
            "camera_id": "123e4567-e89b-12d3-a456-426614174000",
            "source_url": "rtsp://test"
        },
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401


def test_login_and_access_protected_endpoint():
    """Test login and access protected endpoint"""
    # Login
    login_response = client.post("/api/auth/login", json={
        "email": "admin@gtvision.com.br",
        "password": "admin123"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Access protected endpoint
    response = client.post(
        "/api/streams/start",
        json={
            "camera_id": "123e4567-e89b-12d3-a456-426614174000",
            "source_url": "rtsp://test"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code in [201, 400]  # 201 success or 400 business error


def test_rate_limit_on_login():
    """Test rate limiting on login endpoint"""
    for i in range(6):
        response = client.post("/api/auth/login", json={
            "email": "test@test.com",
            "password": "wrong"
        })
        if i < 5:
            assert response.status_code in [401, 429]
        else:
            assert response.status_code == 429
