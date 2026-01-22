"""Timeline response DTO."""
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import List, Dict, Any


class TimelineResponseDTO(BaseModel):
    """Timeline response DTO."""
    timeline_id: UUID
    stream_id: UUID
    start_date: datetime
    end_date: datetime
    segments: List[Dict[str, Any]]
    total_duration_seconds: int
    has_gaps: bool
