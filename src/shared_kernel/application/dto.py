"""Base DTO for application layer."""
from pydantic import BaseModel, ConfigDict


class DTO(BaseModel):
    """Base Data Transfer Object."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
