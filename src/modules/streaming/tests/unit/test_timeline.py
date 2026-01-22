"""Tests for Timeline entity."""
import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from src.streaming.domain.entities.timeline import Timeline
from src.streaming.domain.value_objects.timeline_segment import TimelineSegment


def test_timeline_creation():
    """Test timeline creation."""
    timeline_id = uuid4()
    stream_id = uuid4()
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(hours=2)
    
    timeline = Timeline(
        id=timeline_id,
        stream_id=stream_id,
        start_date=start_date,
        end_date=end_date
    )
    
    assert timeline.id == timeline_id
    assert timeline.stream_id == stream_id
    assert len(timeline.segments) == 0


def test_timeline_add_segment():
    """Test adding segment to timeline."""
    timeline = Timeline(
        id=uuid4(),
        stream_id=uuid4(),
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(hours=2)
    )
    
    segment = TimelineSegment(
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(hours=1),
        has_recording=True
    )
    
    timeline.add_segment(segment)
    
    assert len(timeline.segments) == 1
    assert timeline.segments[0] == segment


def test_timeline_total_duration():
    """Test timeline total duration calculation."""
    timeline = Timeline(
        id=uuid4(),
        stream_id=uuid4(),
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(hours=2)
    )
    
    start = datetime.utcnow()
    timeline.add_segment(TimelineSegment(start, start + timedelta(hours=1), True))
    timeline.add_segment(TimelineSegment(start + timedelta(hours=1), start + timedelta(hours=2), True))
    
    assert timeline.get_total_duration() == 7200


def test_timeline_has_gaps():
    """Test timeline gap detection."""
    timeline = Timeline(
        id=uuid4(),
        stream_id=uuid4(),
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(hours=2)
    )
    
    start = datetime.utcnow()
    timeline.add_segment(TimelineSegment(start, start + timedelta(hours=1), True))
    timeline.add_segment(TimelineSegment(start + timedelta(hours=1), start + timedelta(hours=2), False))
    
    assert timeline.has_gaps()
