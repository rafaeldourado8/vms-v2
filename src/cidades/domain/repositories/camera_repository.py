"""Camera repository interface."""
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from src.cidades.domain.entities.camera import Camera


class CameraRepository(ABC):
    """Camera repository interface."""

    @abstractmethod
    async def save(self, camera: Camera) -> None:
        """Save camera."""
        pass

    @abstractmethod
    async def find_by_id(self, camera_id: UUID) -> Optional[Camera]:
        """Find camera by ID."""
        pass

    @abstractmethod
    async def find_by_cidade(self, cidade_id: UUID) -> List[Camera]:
        """Find all cameras by cidade."""
        pass

    @abstractmethod
    async def delete(self, camera_id: UUID) -> None:
        """Delete camera."""
        pass
