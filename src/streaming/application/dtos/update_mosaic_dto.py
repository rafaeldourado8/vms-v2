"""Update mosaic DTO."""
from uuid import UUID
from pydantic import BaseModel, Field
from typing import List, Optional


class UpdateMosaicDTO(BaseModel):
    """Update mosaic DTO."""
    mosaic_id: UUID
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    layout: Optional[str] = None
    camera_ids: Optional[List[UUID]] = Field(None, max_items=4)
