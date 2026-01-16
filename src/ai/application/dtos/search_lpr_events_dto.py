"""Search LPR events DTO."""
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class SearchLPREventsDTO(BaseModel):
    """Search LPR events DTO."""
    plate: Optional[str] = None
    camera_id: Optional[UUID] = None
    city_id: Optional[UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
