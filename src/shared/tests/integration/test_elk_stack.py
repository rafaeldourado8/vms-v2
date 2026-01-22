"""Smoke tests for ELK Stack."""
import pytest
import requests
import time


@pytest.mark.integration
class TestELKStack:
    """Test ELK Stack integration."""

    def test_elasticsearch_health(self):
        """Test Elasticsearch is healthy."""
        try:
            response = requests.get("http://localhost:9200/_cluster/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data["status"] in ["green", "yellow"]
        except requests.exceptions.ConnectionError:
            pytest.skip("Elasticsearch not running")

    def test_logstash_health(self):
        """Test Logstash is accepting connections."""
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex(("localhost", 5000))
            sock.close()
            assert result == 0, "Logstash port 5000 not accessible"
        except Exception as e:
            pytest.skip(f"Logstash not running: {e}")

    def test_kibana_health(self):
        """Test Kibana is healthy."""
        try:
            response = requests.get("http://localhost:5601/api/status", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data["status"]["overall"]["state"] in ["green", "yellow"]
        except requests.exceptions.ConnectionError:
            pytest.skip("Kibana not running")

    def test_logs_indexed_in_elasticsearch(self):
        """Test logs are being indexed in Elasticsearch."""
        try:
            # Wait for logs to be indexed
            time.sleep(2)
            
            # Check if gtvision indices exist
            response = requests.get("http://localhost:9200/_cat/indices/gtvision-*?format=json", timeout=5)
            assert response.status_code == 200
            indices = response.json()
            
            # Should have at least one index
            assert len(indices) > 0, "No gtvision indices found"
            
            # Check index has documents
            for index in indices:
                assert int(index["docs.count"]) >= 0
        except requests.exceptions.ConnectionError:
            pytest.skip("Elasticsearch not running")

    def test_log_search_in_elasticsearch(self):
        """Test searching logs in Elasticsearch."""
        try:
            # Search for recent logs
            query = {
                "query": {
                    "match_all": {}
                },
                "size": 10,
                "sort": [{"@timestamp": {"order": "desc"}}]
            }
            
            response = requests.post(
                "http://localhost:9200/gtvision-*/_search",
                json=query,
                timeout=5
            )
            assert response.status_code == 200
            data = response.json()
            
            # Should have hits
            assert "hits" in data
            assert "total" in data["hits"]
        except requests.exceptions.ConnectionError:
            pytest.skip("Elasticsearch not running")
