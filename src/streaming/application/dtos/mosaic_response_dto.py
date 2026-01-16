"""Mosaic response DTO."""
from uuid import UUID
from pydantic import BaseModel
from typing import List


class MosaicResponseDTO(BaseModel):
    """Mosaic response DTO."""
    mosaic_id: UUID
    user_id: UUID
    name: str
    layout: str
    camera_ids: List[UUID]
