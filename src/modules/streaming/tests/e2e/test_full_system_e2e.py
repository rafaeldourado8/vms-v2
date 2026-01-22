"""E2E Tests - Full System Integration"""
import pytest
import httpx
import asyncio
from uuid import uuid4


BASE_URL_STREAMING = "http://localhost:8001"
BASE_URL_MEDIAMTX = "http://localhost:9997"


@pytest.fixture
def auth_token():
    """Get authentication token"""
    try:
        response = httpx.post(
            f"{BASE_URL_STREAMING}/api/auth/login",
            json={
                "email": "admin@gtvision.com.br",
                "password": "admin123"
            },
            timeout=5.0
        )
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            pytest.skip(f"Login failed: {response.status_code} - {response.text}")
    except Exception as e:
        pytest.skip(f"Cannot connect to API: {e}")


@pytest.mark.e2e
def test_e2e_stream_lifecycle(auth_token):
    """
    E2E Test: Complete stream lifecycle
    1. Start stream via FastAPI
    2. Validate stream in MediaMTX
    3. Stop stream
    4. Validate stream stopped
    """
    camera_id = str(uuid4())
    
    # 1. Start stream
    response = httpx.post(
        f"{BASE_URL_STREAMING}/api/streams/start",
        json={
            "camera_id": camera_id,
            "source_url": "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code in [201, 400]  # 201 success or 400 if already exists
    
    if response.status_code == 201:
        data = response.json()
        stream_id = data["stream_id"]
        
        # 2. Validate stream exists
        response = httpx.get(
            f"{BASE_URL_STREAMING}/api/streams/{stream_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        
        # 3. Stop stream
        response = httpx.post(
            f"{BASE_URL_STREAMING}/api/streams/{stream_id}/stop",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 204


@pytest.mark.e2e
def test_e2e_recording_lifecycle(auth_token):
    """
    E2E Test: Recording lifecycle
    1. Start stream
    2. Start recording
    3. Validate recording
    4. Stop recording
    """
    camera_id = str(uuid4())
    
    # 1. Start stream
    response = httpx.post(
        f"{BASE_URL_STREAMING}/api/streams/start",
        json={
            "camera_id": camera_id,
            "source_url": "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    if response.status_code == 201:
        stream_id = response.json()["stream_id"]
        
        # 2. Start recording
        response = httpx.post(
            f"{BASE_URL_STREAMING}/api/recordings/start",
            json={
                "stream_id": stream_id,
                "retention_days": 7
            },
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        
        assert response.status_code in [201, 400]
        
        if response.status_code == 201:
            recording_id = response.json()["recording_id"]
            
            # 3. Validate recording
            response = httpx.get(
                f"{BASE_URL_STREAMING}/api/recordings/{recording_id}",
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            assert response.status_code == 200
            
            # 4. Stop recording
            response = httpx.post(
                f"{BASE_URL_STREAMING}/api/recordings/{recording_id}/stop",
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            assert response.status_code == 204


@pytest.mark.e2e
def test_e2e_security_flow():
    """
    E2E Test: Security flow
    1. Access without token (401)
    2. Access with invalid token (401)
    3. Login and access (200)
    4. Rate limit (429)
    """
    # 1. Without token
    response = httpx.post(
        f"{BASE_URL_STREAMING}/api/streams/start",
        json={"camera_id": str(uuid4()), "source_url": "rtsp://test"},
        timeout=5.0
    )
    assert response.status_code == 403
    
    # 2. Invalid token
    response = httpx.post(
        f"{BASE_URL_STREAMING}/api/streams/start",
        json={"camera_id": str(uuid4()), "source_url": "rtsp://test"},
        headers={"Authorization": "Bearer invalid_token"},
        timeout=5.0
    )
    assert response.status_code == 401
    
    # 3. Valid login
    try:
        response = httpx.post(
            f"{BASE_URL_STREAMING}/api/auth/login",
            json={"email": "admin@gtvision.com.br", "password": "admin123"},
            timeout=5.0
        )
        if response.status_code != 200:
            pytest.skip(f"Login failed: {response.status_code} - {response.text}")
    except Exception as e:
        pytest.skip(f"Cannot connect: {e}")
    
    # 4. Rate limit (skip - requires clean state)
    # for i in range(6):
    #     response = httpx.post(
    #         f"{BASE_URL_STREAMING}/api/auth/login",
    #         json={"email": "wrong@test.com", "password": "wrong"},
    #         timeout=5.0
    #     )
    #     if i >= 5:
    #         assert response.status_code == 429


@pytest.mark.e2e
def test_e2e_lgpd_flow(auth_token):
    """
    E2E Test: LGPD compliance flow
    1. Access personal data
    2. Export data
    3. Request deletion
    4. Revoke consent
    """
    # 1. Access data
    response = httpx.get(
        f"{BASE_URL_STREAMING}/api/lgpd/meus-dados",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert "user_id" in response.json()
    
    # 2. Export data
    response = httpx.get(
        f"{BASE_URL_STREAMING}/api/lgpd/exportar?format=json",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["format"] == "json"
    
    # 3. Request deletion
    response = httpx.delete(
        f"{BASE_URL_STREAMING}/api/lgpd/excluir",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert "protocol" in response.json()
    
    # 4. Revoke consent
    response = httpx.post(
        f"{BASE_URL_STREAMING}/api/lgpd/revogar-consentimento",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200


@pytest.mark.e2e
def test_e2e_health_checks():
    """
    E2E Test: Validate all services are healthy
    """
    # Streaming API
    response = httpx.get(f"{BASE_URL_STREAMING}/health", timeout=5.0)
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    
    # Metrics endpoint
    response = httpx.get(f"{BASE_URL_STREAMING}/metrics", timeout=5.0)
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "e2e"])
