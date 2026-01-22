"""Mosaic repository implementation."""
from uuid import UUID
from typing import List, Optional
from src.streaming.domain.entities.mosaic import Mosaic
from src.streaming.domain.repositories.mosaic_repository import MosaicRepository


class MosaicRepositoryImpl(MosaicRepository):
    """In-memory mosaic repository implementation."""
    
    def __init__(self):
        self._mosaics: dict[UUID, Mosaic] = {}
    
    async def save(self, entity: Mosaic) -> Mosaic:
        """Save mosaic."""
        self._mosaics[entity.id] = entity
        return entity
    
    async def find_by_id(self, id: UUID) -> Optional[Mosaic]:
        """Find mosaic by ID."""
        return self._mosaics.get(id)
    
    async def find_all(self) -> List[Mosaic]:
        """Find all mosaics."""
        return list(self._mosaics.values())
    
    async def delete(self, id: UUID) -> bool:
        """Delete mosaic."""
        if id in self._mosaics:
            del self._mosaics[id]
            return True
        return False
    
    async def find_by_user_id(self, user_id: UUID) -> List[Mosaic]:
        """Find mosaics by user ID."""
        return [m for m in self._mosaics.values() if m.user_id == user_id]
