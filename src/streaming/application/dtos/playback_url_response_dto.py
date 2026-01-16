"""Playback URL response DTO."""
from uuid import UUID
from pydantic import BaseModel


class PlaybackUrlResponseDTO(BaseModel):
    """Playback URL response DTO."""
    recording_id: UUID
    playback_url: str
    expires_in: int
