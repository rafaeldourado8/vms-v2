"""Create clip DTO."""
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, validator
from src.shared.domain.domain_exception import DomainException


class CreateClipDTO(BaseModel):
    """Create clip DTO."""
    recording_id: UUID
    start_time: datetime
    end_time: datetime
    
    @validator('end_time')
    def validate_time_range(cls, v, values):
        """Validate time range."""
        if 'start_time' in values and v <= values['start_time']:
            raise DomainException("end_time must be after start_time")
        return v
