"""Testes de integração HAProxy"""
import pytest
import requests


class TestHAProxy:
    BASE_URL = "http://localhost"
    
    def test_stats_available(self):
        response = requests.get(f"{self.BASE_URL}:8404/stats")
        assert response.status_code == 200
        assert "HAProxy" in response.text
    
    def test_health_check(self):
        response = requests.get(f"{self.BASE_URL}/health")
        assert response.status_code == 200
    
    def test_routes_to_streaming(self):
        response = requests.get(f"{self.BASE_URL}/api/streaming/health")
        assert response.status_code == 200
    
    def test_rate_limiting(self):
        responses = []
        for _ in range(101):
            try:
                r = requests.get(f"{self.BASE_URL}/health", timeout=1)
                responses.append(r.status_code)
            except:
                pass
        assert 429 in responses or len(responses) < 101
    
    def test_security_headers(self):
        response = requests.get(f"{self.BASE_URL}/health")
        assert "X-Frame-Options" in response.headers
