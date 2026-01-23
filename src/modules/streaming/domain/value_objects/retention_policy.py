"""Retention policy value object."""
from src.shared.domain.value_object import ValueObject
from src.shared.domain.domain_exception import DomainException


class RetentionPolicy(ValueObject):
    """Retention policy for recordings."""
    
    ALLOWED_DAYS = [7, 15, 30]
    
    def __init__(self, days: int):
        if days not in self.ALLOWED_DAYS:
            raise DomainException(f"Retention days must be one of {self.ALLOWED_DAYS}")
        self._days = days
    
    @property
    def days(self) -> int:
        return self._days
    
    def _get_equality_components(self):
        return [self._days]
