"""Tests for Recording entity."""
import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from src.streaming.domain.entities.recording import Recording
from src.streaming.domain.value_objects.recording_status import RecordingStatus
from src.streaming.domain.value_objects.retention_policy import RetentionPolicy


def test_recording_creation():
    """Test recording creation."""
    recording_id = uuid4()
    stream_id = uuid4()
    retention_policy = RetentionPolicy(7)
    
    recording = Recording(
        id=recording_id,
        stream_id=stream_id,
        retention_policy=retention_policy
    )
    
    assert recording.id == recording_id
    assert recording.stream_id == stream_id
    assert recording.status == RecordingStatus.RECORDING
    assert recording.is_active()


def test_recording_stop():
    """Test recording stop."""
    recording = Recording(
        id=uuid4(),
        stream_id=uuid4(),
        retention_policy=RetentionPolicy(7)
    )
    
    recording.stop()
    
    assert recording.status == RecordingStatus.STOPPED
    assert recording.stopped_at is not None
    assert not recording.is_active()


def test_recording_should_be_deleted():
    """Test recording should be deleted."""
    recording = Recording(
        id=uuid4(),
        stream_id=uuid4(),
        retention_policy=RetentionPolicy(7)
    )
    
    recording.stop()
    recording.stopped_at = datetime.utcnow() - timedelta(days=8)
    
    assert recording.should_be_deleted()


def test_recording_should_not_be_deleted():
    """Test recording should not be deleted."""
    recording = Recording(
        id=uuid4(),
        stream_id=uuid4(),
        retention_policy=RetentionPolicy(7)
    )
    
    recording.stop()
    recording.stopped_at = datetime.utcnow() - timedelta(days=5)
    
    assert not recording.should_be_deleted()
