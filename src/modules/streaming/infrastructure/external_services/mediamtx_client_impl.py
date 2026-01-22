"""MediaMTX client implementation using API v3."""
import httpx
from typing import Optional
from src.modules.streaming.domain.services.mediamtx_client import MediaMTXClient


class MediaMTXClientImpl(MediaMTXClient):
    """MediaMTX client implementation using HTTP API v3."""

    def __init__(self, base_url: str = "http://mediamtx:9997", api_user: str = "mediamtx_api_user", api_pass: str = "GtV!sionMed1aMTX$2025"):
        self.base_url = base_url
        self.auth = (api_user, api_pass)
        self.client = httpx.AsyncClient(timeout=10.0, auth=self.auth)

    async def start_stream(self, stream_id: str, source_url: str) -> bool:
        """Create path in MediaMTX using API v3."""
        try:
            payload = {
                "name": stream_id,
                "source": source_url,
                "sourceOnDemand": True,
                "record": False
            }
            response = await self.client.post(
                f"{self.base_url}/v3/config/paths/add",
                json=payload
            )
            return response.status_code in [200, 201]
        except Exception:
            return False

    async def stop_stream(self, stream_id: str) -> bool:
        """Remove path from MediaMTX using API v3."""
        try:
            response = await self.client.post(
                f"{self.base_url}/v3/config/paths/remove/{stream_id}"
            )
            return response.status_code in [200, 204]
        except Exception:
            return False

    async def get_stream_status(self, stream_id: str) -> dict:
        """Get path status from MediaMTX."""
        try:
            response = await self.client.get(
                f"{self.base_url}/v3/paths/get/{stream_id}"
            )
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception:
            return {}

    async def list_paths(self) -> list[dict]:
        """List all paths in MediaMTX."""
        try:
            response = await self.client.get(f"{self.base_url}/v3/config/paths/list")
            if response.status_code == 200:
                data = response.json()
                return data.get("items", [])
            return []
        except Exception:
            return []

    async def update_path(self, stream_id: str, source_url: str) -> bool:
        """Update path configuration."""
        try:
            payload = {"source": source_url}
            response = await self.client.patch(
                f"{self.base_url}/v3/config/paths/patch/{stream_id}",
                json=payload
            )
            return response.status_code == 200
        except Exception:
            return False

    async def close(self) -> None:
        """Close HTTP client."""
        await self.client.aclose()
