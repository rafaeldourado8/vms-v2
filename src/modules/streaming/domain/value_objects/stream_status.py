"""Stream status enum."""
from enum import Enum


class StreamStatus(Enum):
    """Stream status."""
    
    STOPPED = "STOPPED"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    ERROR = "ERROR"
