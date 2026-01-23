"""Create User DTO."""
from src.shared.application.dto import DTO


class CreateUserDTO(DTO):
    """DTO for creating a user."""

    email: str
    password: str
    name: str
