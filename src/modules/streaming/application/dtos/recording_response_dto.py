"""Recording response DTO."""
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class RecordingResponseDTO(BaseModel):
    """Recording response DTO."""
    recording_id: UUID
    stream_id: UUID
    status: str
    started_at: datetime
    stopped_at: Optional[datetime] = None
    retention_days: int
    storage_path: Optional[str] = None
    file_size_mb: float = 0.0
    duration_seconds: int = 0
