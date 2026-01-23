"""Create mosaic DTO."""
from uuid import UUID
from pydantic import BaseModel, Field, validator
from typing import List
from src.shared.domain.domain_exception import DomainException


class CreateMosaicDTO(BaseModel):
    """Create mosaic DTO."""
    user_id: UUID
    name: str = Field(min_length=1, max_length=100)
    layout: str = Field(default="2x2")
    camera_ids: List[UUID] = Field(default_factory=list, max_items=4)
    
    @validator('camera_ids')
    def validate_cameras(cls, v):
        """Validate camera IDs."""
        if len(v) > 4:
            raise DomainException("Maximum 4 cameras allowed")
        return v
