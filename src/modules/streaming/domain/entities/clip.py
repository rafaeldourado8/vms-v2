"""Clip entity."""
from uuid import UUID
from datetime import datetime
from src.shared.domain.entity import Entity
from src.streaming.domain.value_objects.clip_status import ClipStatus


class Clip(Entity):
    """Clip entity for video clipping."""
    
    def __init__(
        self,
        id: UUID,
        recording_id: UUID,
        start_time: datetime,
        end_time: datetime,
        status: ClipStatus = ClipStatus.PENDING,
        storage_path: str = None,
        file_size_mb: float = 0.0
    ):
        super().__init__(id)
        self.recording_id = recording_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.storage_path = storage_path
        self.file_size_mb = file_size_mb
    
    def mark_processing(self):
        """Mark clip as processing."""
        self.status = ClipStatus.PROCESSING
    
    def mark_completed(self, storage_path: str, file_size_mb: float):
        """Mark clip as completed."""
        self.status = ClipStatus.COMPLETED
        self.storage_path = storage_path
        self.file_size_mb = file_size_mb
    
    def mark_error(self):
        """Mark clip as error."""
        self.status = ClipStatus.ERROR
    
    @property
    def duration_seconds(self) -> int:
        """Get clip duration in seconds."""
        return int((self.end_time - self.start_time).total_seconds())
    
    def is_processing(self) -> bool:
        """Check if clip is processing."""
        return self.status in [ClipStatus.PENDING, ClipStatus.PROCESSING]
