"""Tests for Mosaic entity."""
import pytest
from uuid import uuid4
from src.streaming.domain.entities.mosaic import Mosaic
from src.shared.domain.domain_exception import DomainException


def test_mosaic_creation():
    """Test mosaic creation."""
    mosaic_id = uuid4()
    user_id = uuid4()
    
    mosaic = Mosaic(
        id=mosaic_id,
        user_id=user_id,
        name="My Mosaic",
        layout="2x2"
    )
    
    assert mosaic.id == mosaic_id
    assert mosaic.user_id == user_id
    assert mosaic.name == "My Mosaic"
    assert len(mosaic.camera_ids) == 0


def test_mosaic_add_camera():
    """Test adding camera to mosaic."""
    mosaic = Mosaic(
        id=uuid4(),
        user_id=uuid4(),
        name="Test"
    )
    
    camera_id = uuid4()
    mosaic.add_camera(camera_id)
    
    assert len(mosaic.camera_ids) == 1
    assert camera_id in mosaic.camera_ids


def test_mosaic_max_cameras():
    """Test maximum cameras limit."""
    mosaic = Mosaic(
        id=uuid4(),
        user_id=uuid4(),
        name="Test"
    )
    
    for _ in range(4):
        mosaic.add_camera(uuid4())
    
    with pytest.raises(DomainException, match="Maximum 4 cameras"):
        mosaic.add_camera(uuid4())


def test_mosaic_remove_camera():
    """Test removing camera from mosaic."""
    mosaic = Mosaic(
        id=uuid4(),
        user_id=uuid4(),
        name="Test"
    )
    
    camera_id = uuid4()
    mosaic.add_camera(camera_id)
    mosaic.remove_camera(camera_id)
    
    assert len(mosaic.camera_ids) == 0


def test_mosaic_duplicate_camera():
    """Test adding duplicate camera."""
    mosaic = Mosaic(
        id=uuid4(),
        user_id=uuid4(),
        name="Test"
    )
    
    camera_id = uuid4()
    mosaic.add_camera(camera_id)
    
    with pytest.raises(DomainException, match="already in mosaic"):
        mosaic.add_camera(camera_id)
