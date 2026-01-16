"""Stream repository interface."""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from src.streaming.domain.entities.stream import Stream


class StreamRepository(ABC):
    """Stream repository interface."""

    @abstractmethod
    async def save(self, stream: Stream) -> None:
        """Save stream."""
        pass

    @abstractmethod
    async def find_by_id(self, stream_id: UUID) -> Optional[Stream]:
        """Find stream by ID."""
        pass

    @abstractmethod
    async def find_by_camera_id(self, camera_id: UUID) -> Optional[Stream]:
        """Find stream by camera ID."""
        pass

    @abstractmethod
    async def delete(self, stream_id: UUID) -> None:
        """Delete stream."""
        pass
