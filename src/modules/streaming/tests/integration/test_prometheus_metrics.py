"""Test Prometheus metrics."""
import pytest
import httpx
from src.shared.infrastructure.observability import BusinessMetrics


@pytest.mark.asyncio
async def test_metrics_endpoint():
    """Test /metrics endpoint returns Prometheus format."""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8001/metrics")
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]
        assert b"http_requests_total" in response.content


@pytest.mark.asyncio
async def test_business_metrics():
    """Test business metrics are exposed."""
    # Update metrics
    BusinessMetrics.update_active_streams(5)
    BusinessMetrics.update_active_recordings(3)
    BusinessMetrics.update_cameras_status(online=10, offline=2, total=12)
    BusinessMetrics.increment_lpr_events()
    
    # Fetch metrics
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8001/metrics")
        content = response.content.decode()
        
        assert "gtvision_active_streams 5" in content
        assert "gtvision_recordings_active 3" in content
        assert "gtvision_cameras_online 10" in content
        assert "gtvision_cameras_offline 2" in content
        assert "gtvision_cameras_total 12" in content
        assert "gtvision_lpr_events_total" in content


@pytest.mark.asyncio
async def test_http_metrics_collected():
    """Test HTTP metrics are collected on requests."""
    async with httpx.AsyncClient() as client:
        # Make a request
        await client.get("http://localhost:8001/health")
        
        # Check metrics
        response = await client.get("http://localhost:8001/metrics")
        content = response.content.decode()
        
        assert "http_requests_total" in content
        assert "http_request_duration_seconds" in content
        assert 'endpoint="/health"' in content
