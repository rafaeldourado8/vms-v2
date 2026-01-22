"""Stream response DTO."""
from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class StreamResponseDTO(BaseModel):
    """Stream response DTO."""
    
    id: UUID
    camera_id: UUID
    source_url: str
    status: str
    started_at: Optional[datetime] = None
    stopped_at: Optional[datetime] = None
