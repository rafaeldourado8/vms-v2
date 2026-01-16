"""Integration tests for ClipRepositoryPostgreSQL."""
import pytest
import pytest_asyncio
from uuid import uuid4
from datetime import datetime, timedelta

from streaming.domain.entities.clip import Clip
from streaming.domain.value_objects.clip_status import ClipStatus
from streaming.infrastructure.persistence.clip_repository_postgresql import ClipRepositoryPostgreSQL
from shared_kernel.infrastructure.persistence.connection import get_postgres_connection_string


@pytest_asyncio.fixture
async def repository():
    """Create repository instance."""
    repo = ClipRepositoryPostgreSQL(get_postgres_connection_string())
    yield repo
    await repo.close()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_save_and_find_clip(repository):
    """Test save and find clip."""
    # Arrange
    clip = Clip(
        id=uuid4(),
        recording_id=uuid4(),
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(minutes=5)
    )
    
    # Act
    await repository.save(clip)
    found = await repository.find_by_id(clip.id)
    
    # Assert
    assert found is not None
    assert found.id == clip.id
    assert found.recording_id == clip.recording_id
    assert found.status == ClipStatus.PENDING
    
    # Cleanup
    await repository.delete(clip.id)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_find_by_recording_id(repository):
    """Test find clips by recording ID."""
    # Arrange
    recording_id = uuid4()
    clip1 = Clip(id=uuid4(), recording_id=recording_id, start_time=datetime.now(), end_time=datetime.now() + timedelta(minutes=5))
    clip2 = Clip(id=uuid4(), recording_id=recording_id, start_time=datetime.now(), end_time=datetime.now() + timedelta(minutes=10))
    
    # Act
    await repository.save(clip1)
    await repository.save(clip2)
    found = await repository.find_by_recording_id(recording_id)
    
    # Assert
    assert len(found) >= 2
    found_ids = [c.id for c in found]
    assert clip1.id in found_ids
    assert clip2.id in found_ids
    
    # Cleanup
    await repository.delete(clip1.id)
    await repository.delete(clip2.id)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_list_by_status(repository):
    """Test list clips by status."""
    # Arrange
    clip = Clip(id=uuid4(), recording_id=uuid4(), start_time=datetime.now(), end_time=datetime.now() + timedelta(minutes=5))
    
    # Act
    await repository.save(clip)
    pending = await repository.list_by_status(ClipStatus.PENDING)
    
    # Assert
    assert len(pending) >= 1
    assert any(c.id == clip.id for c in pending)
    
    # Cleanup
    await repository.delete(clip.id)
