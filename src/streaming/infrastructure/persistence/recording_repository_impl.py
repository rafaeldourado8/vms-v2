"""Recording repository implementation."""
from uuid import UUID
from typing import List, Optional
from datetime import datetime
from src.streaming.domain.entities.recording import Recording
from src.streaming.domain.repositories.recording_repository import RecordingRepository
from src.streaming.domain.value_objects.recording_status import RecordingStatus
from src.streaming.domain.value_objects.retention_policy import RetentionPolicy


class RecordingRepositoryImpl(RecordingRepository):
    """In-memory recording repository implementation."""
    
    def __init__(self):
        self._recordings: dict[UUID, Recording] = {}
    
    async def save(self, entity: Recording) -> Recording:
        """Save recording."""
        self._recordings[entity.id] = entity
        return entity
    
    async def find_by_id(self, id: UUID) -> Optional[Recording]:
        """Find recording by ID."""
        return self._recordings.get(id)
    
    async def find_all(self) -> List[Recording]:
        """Find all recordings."""
        return list(self._recordings.values())
    
    async def delete(self, id: UUID) -> bool:
        """Delete recording."""
        if id in self._recordings:
            del self._recordings[id]
            return True
        return False
    
    async def find_by_stream_id(self, stream_id: UUID) -> List[Recording]:
        """Find recordings by stream ID."""
        return [r for r in self._recordings.values() if r.stream_id == stream_id]
    
    async def find_active_by_stream_id(self, stream_id: UUID) -> Optional[Recording]:
        """Find active recording by stream ID."""
        for recording in self._recordings.values():
            if recording.stream_id == stream_id and recording.is_active():
                return recording
        return None
    
    async def search(
        self,
        stream_id: Optional[UUID] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Recording]:
        """Search recordings by filters."""
        results = list(self._recordings.values())
        
        if stream_id:
            results = [r for r in results if r.stream_id == stream_id]
        
        if start_date:
            results = [r for r in results if r.started_at >= start_date]
        
        if end_date:
            results = [r for r in results if r.started_at <= end_date]
        
        return results
    
    async def find_expired(self) -> List[Recording]:
        """Find recordings that should be deleted."""
        return [r for r in self._recordings.values() if r.should_be_deleted()]

    async def count_active(self) -> int:
        """Count active recordings."""
        return sum(1 for r in self._recordings.values() if r.is_active())
