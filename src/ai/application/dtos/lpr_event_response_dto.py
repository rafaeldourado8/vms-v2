"""LPR event response DTO."""
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class LPREventResponseDTO(BaseModel):
    """LPR event response DTO."""
    event_id: UUID
    camera_id: UUID
    plate: str
    confidence: float
    image_url: Optional[str] = None
    detected_at: datetime
    city_id: Optional[UUID] = None
