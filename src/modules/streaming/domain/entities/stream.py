"""Stream entity."""
from uuid import UUID
from datetime import datetime
from src.shared.domain.entity import Entity
from src.streaming.domain.value_objects.stream_status import StreamStatus


class Stream(Entity):
    """Stream entity."""

    def __init__(
        self,
        id: UUID,
        camera_id: UUID,
        source_url: str,
        status: StreamStatus = StreamStatus.STOPPED,
        started_at: datetime = None,
        stopped_at: datetime = None
    ):
        super().__init__(id)
        self.camera_id = camera_id
        self.source_url = source_url
        self.status = status
        self.started_at = started_at
        self.stopped_at = stopped_at

    def start(self):
        """Start stream."""
        self.status = StreamStatus.STARTING
        self.started_at = datetime.utcnow()
        self.stopped_at = None

    def mark_running(self):
        """Mark stream as running."""
        self.status = StreamStatus.RUNNING

    def stop(self):
        """Stop stream."""
        self.status = StreamStatus.STOPPED
        self.stopped_at = datetime.utcnow()

    def mark_error(self):
        """Mark stream as error."""
        self.status = StreamStatus.ERROR

    def is_active(self) -> bool:
        """Check if stream is active."""
        return self.status in [StreamStatus.STARTING, StreamStatus.RUNNING]
