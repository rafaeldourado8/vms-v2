"""Mosaic repository interface."""
from abc import abstractmethod
from uuid import UUID
from typing import List, Optional
from src.shared.domain.repository import Repository
from src.streaming.domain.entities.mosaic import Mosaic


class MosaicRepository(Repository[Mosaic]):
    """Mosaic repository interface."""
    
    @abstractmethod
    async def find_by_user_id(self, user_id: UUID) -> List[Mosaic]:
        """Find mosaics by user ID."""
        pass
