"""Limite de Câmeras value object."""
from src.shared_kernel.domain.domain_exception import ValidationException
from src.shared_kernel.domain.value_object import ValueObject


class LimiteCameras(ValueObject):
    """Limite de câmeras value object."""

    MAX_CAMERAS = 1000

    def __init__(self, value: int) -> None:
        """Initialize limite."""
        self._validate(value)
        self.value = value

    def _validate(self, value: int) -> None:
        """Validate limite."""
        if value < 0:
            raise ValidationException("Limite cannot be negative")
        if value > self.MAX_CAMERAS:
            raise ValidationException(f"Limite cannot exceed {self.MAX_CAMERAS}")

    def __str__(self) -> str:
        """String representation."""
        return str(self.value)
