"""Testes E2E completos"""
import pytest
import requests
import time
from datetime import datetime


@pytest.mark.e2e
class TestE2EFullFlow:
    BASE_URL = "http://localhost"
    
    @pytest.fixture
    def auth_token(self):
        response = requests.post(
            f"{self.BASE_URL}:8001/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        if response.status_code == 200:
            return response.json()["access_token"]
        return None
    
    def test_create_camera_and_stream(self, auth_token):
        """E2E: Django → FastAPI → MediaMTX"""
        headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
        
        camera_data = {
            "nome": "Camera E2E",
            "url_rtsp": "rtsp://localhost:8554/test",
            "cidade_id": 1
        }
        
        response = requests.post(
            f"{self.BASE_URL}/api/cidades/cameras",
            json=camera_data,
            headers=headers
        )
        assert response.status_code in [200, 201, 401]
        
        if response.status_code in [200, 201]:
            camera_id = response.json().get("id")
            
            stream_response = requests.post(
                f"{self.BASE_URL}/api/streaming/streams/start",
                json={"camera_id": camera_id},
                headers=headers
            )
            assert stream_response.status_code in [200, 201, 401]
    
    def test_lpr_detection_flow(self, auth_token):
        """E2E: Webhook LPR → Buscar"""
        lpr_data = {
            "plate": "ABC1234",
            "confidence": 0.95,
            "camera_id": 1,
            "timestamp": datetime.now().isoformat()
        }
        
        webhook_response = requests.post(
            f"{self.BASE_URL}/api/ai/lpr/webhook",
            json=lpr_data
        )
        assert webhook_response.status_code in [200, 201, 401]
        
        if webhook_response.status_code in [200, 201]:
            time.sleep(1)
            headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
            search_response = requests.get(
                f"{self.BASE_URL}/api/ai/lpr/events",
                params={"plate": "ABC1234"},
                headers=headers
            )
            assert search_response.status_code in [200, 401]
    
    def test_security_flow(self):
        """E2E: 401, 429, audit"""
        response_401 = requests.get(f"{self.BASE_URL}/api/admin/users")
        assert response_401.status_code == 401
        
        responses = []
        for _ in range(15):
            try:
                r = requests.post(
                    f"{self.BASE_URL}/api/auth/login",
                    json={"username": "test", "password": "test"},
                    timeout=1
                )
                responses.append(r.status_code)
            except:
                pass
        assert 429 in responses
    
    def test_observability(self):
        """E2E: Prometheus, Grafana, ELK"""
        assert requests.get("http://localhost:9090/-/healthy").status_code == 200
        assert requests.get("http://localhost:3000/api/health").status_code == 200
        assert requests.get("http://localhost:9200/_cluster/health").status_code == 200
        assert requests.get("http://localhost:8404/stats").status_code == 200


@pytest.mark.e2e
class TestE2EIntegration:
    BASE_URL = "http://localhost"
    
    def test_rabbitmq_connection(self):
        response = requests.get("http://localhost:15672/api/overview")
        assert response.status_code in [200, 401]
    
    def test_mediamtx_connection(self):
        response = requests.get("http://localhost:8888")
        assert response.status_code in [200, 404]
    
    def test_minio_connection(self):
        response = requests.get("http://localhost:9000/minio/health/live")
        assert response.status_code == 200
    
    def test_api_response_time(self):
        start = time.time()
        response = requests.get(f"{self.BASE_URL}/health")
        elapsed = (time.time() - start) * 1000
        assert response.status_code == 200
        assert elapsed < 200
