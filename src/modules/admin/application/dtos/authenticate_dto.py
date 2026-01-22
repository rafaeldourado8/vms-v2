"""Authenticate DTO."""
from src.shared_kernel.application.dto import DTO


class AuthenticateDTO(DTO):
    """DTO for user authentication."""

    email: str
    password: str
