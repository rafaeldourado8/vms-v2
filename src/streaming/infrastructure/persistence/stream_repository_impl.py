"""Stream repository implementation."""
from typing import Optional, Dict
from uuid import UUID
from src.streaming.domain.entities.stream import Stream
from src.streaming.domain.repositories.stream_repository import StreamRepository


class StreamRepositoryImpl(StreamRepository):
    """In-memory stream repository implementation."""

    def __init__(self):
        self._streams: Dict[UUID, Stream] = {}

    async def save(self, stream: Stream) -> None:
        """Save stream."""
        self._streams[stream.id] = stream

    async def find_by_id(self, stream_id: UUID) -> Optional[Stream]:
        """Find stream by ID."""
        return self._streams.get(stream_id)

    async def find_by_camera_id(self, camera_id: UUID) -> Optional[Stream]:
        """Find stream by camera ID."""
        for stream in self._streams.values():
            if stream.camera_id == camera_id:
                return stream
        return None

    async def delete(self, stream_id: UUID) -> None:
        """Delete stream."""
        if stream_id in self._streams:
            del self._streams[stream_id]
