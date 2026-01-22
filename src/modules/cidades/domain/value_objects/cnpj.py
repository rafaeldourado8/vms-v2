"""CNPJ value object."""
import re

from src.shared_kernel.domain.domain_exception import ValidationException
from src.shared_kernel.domain.value_object import ValueObject


class CNPJ(ValueObject):
    """CNPJ value object with validation."""

    def __init__(self, value: str) -> None:
        """Initialize CNPJ."""
        self._validate(value)
        self.value = self._format(value)

    def _validate(self, value: str) -> None:
        """Validate CNPJ format."""
        if not value:
            raise ValidationException("CNPJ cannot be empty")
        
        # Remove non-digits
        digits = re.sub(r"\D", "", value)
        
        if len(digits) != 14:
            raise ValidationException("CNPJ must have 14 digits")

    def _format(self, value: str) -> str:
        """Format CNPJ (remove non-digits)."""
        return re.sub(r"\D", "", value)

    def __str__(self) -> str:
        """String representation with mask."""
        v = self.value
        return f"{v[:2]}.{v[2:5]}.{v[5:8]}/{v[8:12]}-{v[12:]}"
