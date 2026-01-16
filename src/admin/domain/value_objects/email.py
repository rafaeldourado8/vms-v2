"""Email value object."""
import re

from src.shared_kernel.domain.domain_exception import ValidationException
from src.shared_kernel.domain.value_object import ValueObject


class Email(ValueObject):
    """Email value object with validation."""

    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def __init__(self, value: str) -> None:
        """Initialize email."""
        self._validate(value)
        self.value = value.lower().strip()

    def _validate(self, value: str) -> None:
        """Validate email format."""
        if not value or not value.strip():
            raise ValidationException("Email cannot be empty")
        if not re.match(self.EMAIL_REGEX, value):
            raise ValidationException(f"Invalid email format: {value}")

    def __str__(self) -> str:
        """String representation."""
        return self.value
