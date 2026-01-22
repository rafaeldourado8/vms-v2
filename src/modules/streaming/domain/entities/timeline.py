"""Timeline entity."""
from uuid import UUID
from datetime import datetime
from typing import List
from src.shared_kernel.domain.entity import Entity
from src.streaming.domain.value_objects.timeline_segment import TimelineSegment


class Timeline(Entity):
    """Timeline entity for recording playback."""
    
    def __init__(
        self,
        id: UUID,
        stream_id: UUID,
        start_date: datetime,
        end_date: datetime,
        segments: List[TimelineSegment] = None
    ):
        super().__init__(id)
        self.stream_id = stream_id
        self.start_date = start_date
        self.end_date = end_date
        self.segments = segments or []
    
    def add_segment(self, segment: TimelineSegment):
        """Add segment to timeline."""
        self.segments.append(segment)
    
    def get_total_duration(self) -> int:
        """Get total duration in seconds."""
        return sum(s.duration_seconds for s in self.segments if s.has_recording)
    
    def has_gaps(self) -> bool:
        """Check if timeline has gaps."""
        return any(not s.has_recording for s in self.segments)
