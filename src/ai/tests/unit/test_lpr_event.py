"""Tests for LPREvent entity."""
import pytest
from uuid import uuid4
from datetime import datetime
from src.ai.domain.entities.lpr_event import LPREvent


def test_lpr_event_creation():
    """Test LPR event creation."""
    event_id = uuid4()
    camera_id = uuid4()
    
    event = LPREvent(
        id=event_id,
        camera_id=camera_id,
        plate="ABC1234",
        confidence=0.95
    )
    
    assert event.id == event_id
    assert event.camera_id == camera_id
    assert event.plate == "ABC1234"
    assert event.confidence == 0.95


def test_lpr_event_plate_uppercase():
    """Test plate is converted to uppercase."""
    event = LPREvent(
        id=uuid4(),
        camera_id=uuid4(),
        plate="abc1234",
        confidence=0.95
    )
    
    assert event.plate == "ABC1234"


def test_lpr_event_high_confidence():
    """Test high confidence detection."""
    event = LPREvent(
        id=uuid4(),
        camera_id=uuid4(),
        plate="ABC1234",
        confidence=0.85
    )
    
    assert event.is_high_confidence()


def test_lpr_event_low_confidence():
    """Test low confidence detection."""
    event = LPREvent(
        id=uuid4(),
        camera_id=uuid4(),
        plate="ABC1234",
        confidence=0.65
    )
    
    assert not event.is_high_confidence()
