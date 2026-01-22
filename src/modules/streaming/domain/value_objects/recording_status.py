"""Recording status enum."""
from enum import Enum


class RecordingStatus(Enum):
    """Recording status."""
    RECORDING = "RECORDING"
    STOPPED = "STOPPED"
    ERROR = "ERROR"
