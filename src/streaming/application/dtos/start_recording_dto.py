"""Start recording DTO."""
from uuid import UUID
from pydantic import BaseModel, Field


class StartRecordingDTO(BaseModel):
    """Start recording DTO."""
    stream_id: UUID
    retention_days: int = Field(default=7, ge=7, le=30)
