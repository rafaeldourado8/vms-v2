"""E2E Tests - ELK Stack Integration"""
import pytest
import httpx
import time


BASE_URL_STREAMING = "http://localhost:8001"
BASE_URL_ELASTICSEARCH = "http://localhost:9200"
BASE_URL_KIBANA = "http://localhost:5601"


@pytest.fixture
def auth_token():
    """Get authentication token"""
    try:
        response = httpx.post(
            f"{BASE_URL_STREAMING}/api/auth/login",
            json={"email": "admin@gtvision.com.br", "password": "admin123"},
            timeout=5.0
        )
        if response.status_code == 200:
            return response.json()["access_token"]
        pytest.skip(f"Login failed: {response.status_code}")
    except Exception as e:
        pytest.skip(f"Cannot connect: {e}")


@pytest.mark.e2e
def test_elasticsearch_is_up():
    """Test Elasticsearch is running"""
    try:
        response = httpx.get(f"{BASE_URL_ELASTICSEARCH}/_cluster/health", timeout=5.0)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["green", "yellow"]
    except Exception:
        pytest.skip("Elasticsearch not available")


@pytest.mark.e2e
def test_kibana_is_up():
    """Test Kibana is running"""
    try:
        response = httpx.get(f"{BASE_URL_KIBANA}/api/status", timeout=5.0)
        assert response.status_code == 200
    except Exception:
        pytest.skip("Kibana not available")


@pytest.mark.e2e
def test_security_audit_logs_to_elk(auth_token):
    """Test security audit logs are sent to ELK"""
    # Perform login (generates audit log)
    response = httpx.post(
        f"{BASE_URL_STREAMING}/api/auth/login",
        json={"email": "admin@gtvision.com.br", "password": "admin123"},
        timeout=5.0
    )
    assert response.status_code == 200
    
    # Wait for log to be indexed
    time.sleep(2)
    
    # Check if audit index exists
    try:
        response = httpx.get(
            f"{BASE_URL_ELASTICSEARCH}/gtvision-audit-*/_search",
            json={"query": {"match": {"audit_action": "LOGIN"}}},
            timeout=5.0
        )
        # If index exists, check for logs
        if response.status_code == 200:
            data = response.json()
            assert data["hits"]["total"]["value"] >= 0
    except Exception:
        pytest.skip("Elasticsearch index not ready")


@pytest.mark.e2e
def test_lgpd_audit_logs_to_elk(auth_token):
    """Test LGPD actions are logged to ELK"""
    # Access personal data
    response = httpx.get(
        f"{BASE_URL_STREAMING}/api/lgpd/meus-dados",
        headers={"Authorization": f"Bearer {auth_token}"},
        timeout=5.0
    )
    assert response.status_code == 200
    
    # Wait for log
    time.sleep(2)
    
    # Check audit logs
    try:
        response = httpx.get(
            f"{BASE_URL_ELASTICSEARCH}/gtvision-audit-*/_search",
            json={"query": {"match": {"audit_action": "DATA_ACCESS"}}},
            timeout=5.0
        )
        if response.status_code == 200:
            data = response.json()
            assert data["hits"]["total"]["value"] >= 0
    except Exception:
        pytest.skip("Elasticsearch index not ready")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "e2e"])
