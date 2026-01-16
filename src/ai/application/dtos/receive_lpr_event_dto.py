"""Receive LPR event DTO."""
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class ReceiveLPREventDTO(BaseModel):
    """Receive LPR event DTO."""
    camera_id: UUID
    plate: str = Field(min_length=7, max_length=8)
    confidence: float = Field(ge=0.0, le=1.0)
    image_base64: Optional[str] = None
    detected_at: Optional[datetime] = None
    city_id: Optional[UUID] = None
