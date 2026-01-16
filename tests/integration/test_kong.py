"""Testes de integração Kong Gateway"""
import pytest
import requests


class TestKong:
    BASE_URL = "http://localhost:8000"
    
    def test_kong_health(self):
        response = requests.get(f"{self.BASE_URL}/health")
        assert response.status_code in [200, 404]
    
    def test_kong_routes_admin(self):
        response = requests.get(f"{self.BASE_URL}/api/admin/users")
        assert response.status_code in [200, 401]
    
    def test_kong_routes_streaming(self):
        response = requests.get(f"{self.BASE_URL}/api/streaming/health")
        assert response.status_code in [200, 401]
    
    def test_kong_rate_limiting(self):
        responses = []
        for _ in range(15):
            try:
                r = requests.post(f"{self.BASE_URL}/api/auth/login", json={}, timeout=1)
                responses.append(r.status_code)
            except:
                pass
        assert 429 in responses
    
    def test_kong_cors_headers(self):
        response = requests.options(
            f"{self.BASE_URL}/api/streaming/health",
            headers={"Origin": "http://localhost:5173"}
        )
        assert "Access-Control-Allow-Origin" in response.headers
    
    def test_kong_jwt_required(self):
        response = requests.get(f"{self.BASE_URL}/api/admin/users")
        assert response.status_code == 401
