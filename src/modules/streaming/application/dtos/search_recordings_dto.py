"""Search recordings DTO."""
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class SearchRecordingsDTO(BaseModel):
    """Search recordings DTO."""
    stream_id: Optional[UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
