"""Generate thumbnails DTO."""
from uuid import UUID
from pydantic import BaseModel, Field


class GenerateThumbnailsDTO(BaseModel):
    """Generate thumbnails DTO."""
    recording_id: UUID
    interval_seconds: int = Field(default=60, ge=10, le=300)
