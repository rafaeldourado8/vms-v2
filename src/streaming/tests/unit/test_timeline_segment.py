"""Tests for TimelineSegment value object."""
import pytest
from datetime import datetime, timedelta
from src.streaming.domain.value_objects.timeline_segment import TimelineSegment


def test_timeline_segment_creation():
    """Test timeline segment creation."""
    start = datetime.utcnow()
    end = start + timedelta(hours=1)
    
    segment = TimelineSegment(start, end, True)
    
    assert segment.start_time == start
    assert segment.end_time == end
    assert segment.has_recording is True


def test_timeline_segment_duration():
    """Test timeline segment duration calculation."""
    start = datetime.utcnow()
    end = start + timedelta(hours=1)
    
    segment = TimelineSegment(start, end, True)
    
    assert segment.duration_seconds == 3600


def test_timeline_segment_equality():
    """Test timeline segment equality."""
    start = datetime.utcnow()
    end = start + timedelta(hours=1)
    
    segment1 = TimelineSegment(start, end, True)
    segment2 = TimelineSegment(start, end, True)
    segment3 = TimelineSegment(start, end, False)
    
    assert segment1 == segment2
    assert segment1 != segment3
