"""Smoke tests for observability stack."""
import pytest
import httpx
import asyncio


@pytest.mark.asyncio
async def test_prometheus_is_up():
    """Test Prometheus is running and accessible."""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:9090/-/healthy")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_prometheus_scraping_streaming_api():
    """Test Prometheus is scraping streaming API metrics."""
    async with httpx.AsyncClient() as client:
        # Wait for scrape
        await asyncio.sleep(2)
        
        response = await client.get("http://localhost:9090/api/v1/targets")
        assert response.status_code == 200
        
        data = response.json()
        targets = data.get("data", {}).get("activeTargets", [])
        
        streaming_target = next((t for t in targets if t["labels"]["job"] == "streaming"), None)
        assert streaming_target is not None
        assert streaming_target["health"] == "up"


@pytest.mark.asyncio
async def test_grafana_is_up():
    """Test Grafana is running and accessible."""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:3000/api/health")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_grafana_datasource_configured():
    """Test Grafana has Prometheus datasource configured."""
    async with httpx.AsyncClient(auth=("admin", "admin")) as client:
        response = await client.get("http://localhost:3000/api/datasources")
        assert response.status_code == 200
        
        datasources = response.json()
        prometheus_ds = next((ds for ds in datasources if ds["type"] == "prometheus"), None)
        assert prometheus_ds is not None
        assert prometheus_ds["name"] == "Prometheus"


@pytest.mark.asyncio
async def test_metrics_endpoint_available():
    """Test streaming API /metrics endpoint is available."""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8001/metrics")
        assert response.status_code == 200
        assert b"http_requests_total" in response.content
        assert b"gtvision_active_streams" in response.content
