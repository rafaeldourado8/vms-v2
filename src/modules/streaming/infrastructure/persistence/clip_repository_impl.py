"""Clip repository implementation."""
from uuid import UUID
from typing import List, Optional
from src.streaming.domain.entities.clip import Clip
from src.streaming.domain.repositories.clip_repository import ClipRepository
from src.streaming.domain.value_objects.clip_status import ClipStatus


class ClipRepositoryImpl(ClipRepository):
    """In-memory clip repository implementation."""
    
    def __init__(self):
        self._clips: dict[UUID, Clip] = {}
    
    async def save(self, entity: Clip) -> Clip:
        """Save clip."""
        self._clips[entity.id] = entity
        return entity
    
    async def find_by_id(self, id: UUID) -> Optional[Clip]:
        """Find clip by ID."""
        return self._clips.get(id)
    
    async def find_all(self) -> List[Clip]:
        """Find all clips."""
        return list(self._clips.values())
    
    async def delete(self, id: UUID) -> bool:
        """Delete clip."""
        if id in self._clips:
            del self._clips[id]
            return True
        return False
    
    async def find_by_recording_id(self, recording_id: UUID) -> List[Clip]:
        """Find clips by recording ID."""
        return [c for c in self._clips.values() if c.recording_id == recording_id]
    
    async def find_pending(self) -> List[Clip]:
        """Find pending clips for processing."""
        return [c for c in self._clips.values() if c.status == ClipStatus.PENDING]
