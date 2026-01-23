"""Assign Role DTO."""
from uuid import UUID

from src.shared.application.dto import DTO


class AssignRoleDTO(DTO):
    """DTO for assigning role to user."""

    user_id: UUID
    role_code: str
