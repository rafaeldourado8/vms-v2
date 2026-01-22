"""User Response DTO."""
from typing import List
from uuid import UUID

from src.shared_kernel.application.dto import DTO


class UserResponseDTO(DTO):
    """DTO for user response."""

    id: UUID
    email: str
    name: str
    is_active: bool
    roles: List[str]
