"""Authenticate DTO."""
from src.shared.application.dto import DTO


class AuthenticateDTO(DTO):
    """DTO for user authentication."""

    email: str
    password: str
