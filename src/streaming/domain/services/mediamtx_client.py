"""MediaMTX client interface."""
from abc import ABC, abstractmethod


class MediaMTXClient(ABC):
    """MediaMTX client interface."""

    @abstractmethod
    async def start_stream(self, stream_id: str, source_url: str) -> bool:
        """Start stream in MediaMTX."""
        pass

    @abstractmethod
    async def stop_stream(self, stream_id: str) -> bool:
        """Stop stream in MediaMTX."""
        pass

    @abstractmethod
    async def get_stream_status(self, stream_id: str) -> dict:
        """Get stream status from MediaMTX."""
        pass
