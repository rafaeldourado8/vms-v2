"""Clip status enum."""
from enum import Enum


class ClipStatus(Enum):
    """Clip status."""
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
