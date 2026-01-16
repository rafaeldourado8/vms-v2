"""MediaMTX client implementation."""
import httpx
from typing import Optional
from src.streaming.domain.services.mediamtx_client import MediaMTXClient


class MediaMTXClientImpl(MediaMTXClient):
    """MediaMTX client implementation using HTTP API."""

    def __init__(self, base_url: str = "http://mediamtx:9997"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=10.0)

    async def start_stream(self, stream_id: str, source_url: str) -> bool:
        """Start stream in MediaMTX."""
        try:
            payload = {
                "name": stream_id,
                "source": source_url,
                "sourceProtocol": "automatic",
                "sourceOnDemand": False
            }
            response = await self.client.post(
                f"{self.base_url}/v3/config/paths/add/{stream_id}",
                json=payload
            )
            return response.status_code in [200, 201]
        except Exception:
            return False

    async def stop_stream(self, stream_id: str) -> bool:
        """Stop stream in MediaMTX."""
        try:
            response = await self.client.delete(
                f"{self.base_url}/v3/config/paths/delete/{stream_id}"
            )
            return response.status_code in [200, 204]
        except Exception:
            return False

    async def get_stream_status(self, stream_id: str) -> dict:
        """Get stream status from MediaMTX."""
        try:
            response = await self.client.get(
                f"{self.base_url}/v3/paths/get/{stream_id}"
            )
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception:
            return {}
