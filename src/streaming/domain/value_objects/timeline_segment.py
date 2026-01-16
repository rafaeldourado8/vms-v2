"""Timeline segment value object."""
from datetime import datetime
from src.shared_kernel.domain.value_object import ValueObject


class TimelineSegment(ValueObject):
    """Timeline segment representing a period with recording."""
    
    def __init__(self, start_time: datetime, end_time: datetime, has_recording: bool = True):
        self._start_time = start_time
        self._end_time = end_time
        self._has_recording = has_recording
    
    @property
    def start_time(self) -> datetime:
        return self._start_time
    
    @property
    def end_time(self) -> datetime:
        return self._end_time
    
    @property
    def has_recording(self) -> bool:
        return self._has_recording
    
    @property
    def duration_seconds(self) -> int:
        return int((self._end_time - self._start_time).total_seconds())
    
    def _get_equality_components(self):
        return [self._start_time, self._end_time, self._has_recording]
