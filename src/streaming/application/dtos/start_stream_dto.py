"""Start stream DTO."""
from uuid import UUID
from pydantic import BaseModel, Field


class StartStreamDTO(BaseModel):
    """Start stream input DTO."""
    
    camera_id: UUID = Field(..., description="Camera ID")
    source_url: str = Field(..., description="RTSP/RTMP source URL")
