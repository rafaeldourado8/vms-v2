"""Recording entity."""
from uuid import UUID
from datetime import datetime
from src.shared.domain.entity import Entity
from src.streaming.domain.value_objects.recording_status import RecordingStatus
from src.streaming.domain.value_objects.retention_policy import RetentionPolicy


class Recording(Entity):
    """Recording entity."""
    
    def __init__(
        self,
        id: UUID,
        stream_id: UUID,
        retention_policy: RetentionPolicy,
        status: RecordingStatus = RecordingStatus.RECORDING,
        started_at: datetime = None,
        stopped_at: datetime = None,
        storage_path: str = None,
        file_size_mb: float = 0.0,
        duration_seconds: int = 0
    ):
        super().__init__(id)
        self.stream_id = stream_id
        self.retention_policy = retention_policy
        self.status = status
        self.started_at = started_at or datetime.utcnow()
        self.stopped_at = stopped_at
        self.storage_path = storage_path
        self.file_size_mb = file_size_mb
        self.duration_seconds = duration_seconds
    
    def stop(self):
        """Stop recording."""
        self.status = RecordingStatus.STOPPED
        self.stopped_at = datetime.utcnow()
        if self.started_at:
            self.duration_seconds = int((self.stopped_at - self.started_at).total_seconds())
    
    def mark_error(self):
        """Mark recording as error."""
        self.status = RecordingStatus.ERROR
    
    def is_active(self) -> bool:
        """Check if recording is active."""
        return self.status == RecordingStatus.RECORDING
    
    def should_be_deleted(self) -> bool:
        """Check if recording should be deleted based on retention policy."""
        if not self.stopped_at:
            return False
        days_old = (datetime.utcnow() - self.stopped_at).days
        return days_old > self.retention_policy.days
