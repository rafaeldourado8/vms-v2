"""Get timeline DTO."""
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class GetTimelineDTO(BaseModel):
    """Get timeline DTO."""
    stream_id: UUID
    start_date: datetime
    end_date: datetime
