"""E2E tests for LGPD compliance"""
import pytest
from fastapi.testclient import TestClient
from src.streaming.infrastructure.web.main import app

client = TestClient(app)


def get_auth_token():
    """Helper to get auth token"""
    response = client.post("/api/auth/login", json={
        "email": "admin@gtvision.com.br",
        "password": "admin123"
    })
    return response.json()["access_token"]


def test_lgpd_data_access():
    """Test LGPD right to access data"""
    token = get_auth_token()
    
    response = client.get(
        "/api/lgpd/meus-dados",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "email" in data
    assert "data_processing" in data


def test_lgpd_data_export():
    """Test LGPD right to data portability"""
    token = get_auth_token()
    
    response = client.get(
        "/api/lgpd/exportar?format=json",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["format"] == "json"
    assert "exported_at" in data


def test_lgpd_data_deletion():
    """Test LGPD right to deletion"""
    token = get_auth_token()
    
    response = client.delete(
        "/api/lgpd/excluir",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "protocol" in data
    assert data["status"] == "pending"


def test_lgpd_consent_revocation():
    """Test LGPD right to revoke consent"""
    token = get_auth_token()
    
    response = client.post(
        "/api/lgpd/revogar-consentimento",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "revoked_at" in data


def test_lgpd_without_auth():
    """Test LGPD endpoints require authentication"""
    response = client.get("/api/lgpd/meus-dados")
    assert response.status_code == 403
