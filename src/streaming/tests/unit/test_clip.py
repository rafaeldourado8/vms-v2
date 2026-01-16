"""Tests for Clip entity."""
import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from src.streaming.domain.entities.clip import Clip
from src.streaming.domain.value_objects.clip_status import ClipStatus


def test_clip_creation():
    """Test clip creation."""
    clip_id = uuid4()
    recording_id = uuid4()
    start_time = datetime.utcnow()
    end_time = start_time + timedelta(minutes=5)
    
    clip = Clip(
        id=clip_id,
        recording_id=recording_id,
        start_time=start_time,
        end_time=end_time
    )
    
    assert clip.id == clip_id
    assert clip.recording_id == recording_id
    assert clip.status == ClipStatus.PENDING
    assert clip.duration_seconds == 300


def test_clip_mark_processing():
    """Test clip mark processing."""
    clip = Clip(
        id=uuid4(),
        recording_id=uuid4(),
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(minutes=5)
    )
    
    clip.mark_processing()
    
    assert clip.status == ClipStatus.PROCESSING
    assert clip.is_processing()


def test_clip_mark_completed():
    """Test clip mark completed."""
    clip = Clip(
        id=uuid4(),
        recording_id=uuid4(),
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(minutes=5)
    )
    
    clip.mark_completed("/clips/test.mp4", 10.5)
    
    assert clip.status == ClipStatus.COMPLETED
    assert clip.storage_path == "/clips/test.mp4"
    assert clip.file_size_mb == 10.5
    assert not clip.is_processing()


def test_clip_mark_error():
    """Test clip mark error."""
    clip = Clip(
        id=uuid4(),
        recording_id=uuid4(),
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(minutes=5)
    )
    
    clip.mark_error()
    
    assert clip.status == ClipStatus.ERROR
