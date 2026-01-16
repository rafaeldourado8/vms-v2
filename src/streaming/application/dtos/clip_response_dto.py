"""Clip response DTO."""
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ClipResponseDTO(BaseModel):
    """Clip response DTO."""
    clip_id: UUID
    recording_id: UUID
    start_time: datetime
    end_time: datetime
    status: str
    storage_path: Optional[str] = None
    file_size_mb: float = 0.0
    duration_seconds: int
    created_at: datetime
