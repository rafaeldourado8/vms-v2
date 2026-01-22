"""Thumbnail response DTO."""
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class ThumbnailResponseDTO(BaseModel):
    """Thumbnail response DTO."""
    recording_id: UUID
    url: str
    timestamp: datetime
