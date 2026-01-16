"""Create User DTO."""
from src.shared_kernel.application.dto import DTO


class CreateUserDTO(DTO):
    """DTO for creating a user."""

    email: str
    password: str
    name: str
