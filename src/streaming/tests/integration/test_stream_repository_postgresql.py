"""Integration tests for StreamRepositoryPostgreSQL."""
import pytest
import pytest_asyncio
from uuid import uuid4
from datetime import datetime

from streaming.domain.entities.stream import Stream
from streaming.domain.value_objects.stream_status import StreamStatus
from streaming.infrastructure.persistence.stream_repository_postgresql import StreamRepositoryPostgreSQL
from shared_kernel.infrastructure.persistence.connection import get_postgres_connection_string


@pytest_asyncio.fixture
async def repository():
    """Create repository instance."""
    repo = StreamRepositoryPostgreSQL(get_postgres_connection_string())
    yield repo
    await repo.close()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_save_and_find_stream(repository):
    """Test save and find stream."""
    # Arrange
    stream = Stream(
        id=uuid4(),
        camera_id=uuid4(),
        source_url="rtsp://test-camera/stream"
    )
    stream.start()
    stream.mark_running()  # Marcar como RUNNING
    
    # Act
    await repository.save(stream)
    found = await repository.find_by_id(stream.id)
    
    # Assert
    assert found is not None
    assert found.id == stream.id
    assert found.camera_id == stream.camera_id
    assert found.source_url == stream.source_url
    assert found.status == StreamStatus.RUNNING
    
    # Cleanup
    await repository.delete(stream.id)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_find_by_camera_id(repository):
    """Test find stream by camera ID."""
    # Arrange
    camera_id = uuid4()
    stream = Stream(
        id=uuid4(),
        camera_id=camera_id,
        source_url="rtsp://test-camera/stream"
    )
    stream.start()
    stream.mark_running()  # Marcar como RUNNING
    
    # Act
    await repository.save(stream)
    found = await repository.find_by_camera_id(camera_id)
    
    # Assert
    assert found is not None
    assert found.camera_id == camera_id
    assert found.status == StreamStatus.RUNNING
    
    # Cleanup
    await repository.delete(stream.id)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_list_active_streams(repository):
    """Test list active streams."""
    # Arrange
    stream1 = Stream(id=uuid4(), camera_id=uuid4(), source_url="rtsp://cam1")
    stream1.start()
    stream1.mark_running()  # Marcar como RUNNING
    
    stream2 = Stream(id=uuid4(), camera_id=uuid4(), source_url="rtsp://cam2")
    stream2.start()
    stream2.mark_running()  # Marcar como RUNNING
    
    # Act
    await repository.save(stream1)
    await repository.save(stream2)
    active = await repository.list_active()
    
    # Assert
    assert len(active) >= 2
    active_ids = [s.id for s in active]
    assert stream1.id in active_ids
    assert stream2.id in active_ids
    
    # Cleanup
    await repository.delete(stream1.id)
    await repository.delete(stream2.id)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_update_stream_status(repository):
    """Test update stream status."""
    # Arrange
    stream = Stream(id=uuid4(), camera_id=uuid4(), source_url="rtsp://test")
    stream.start()
    await repository.save(stream)
    
    # Act
    stream.stop()
    await repository.save(stream)
    found = await repository.find_by_id(stream.id)
    
    # Assert
    assert found is not None
    assert found.status == StreamStatus.STOPPED
    assert found.stopped_at is not None
    
    # Cleanup
    await repository.delete(stream.id)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_delete_stream(repository):
    """Test delete stream."""
    # Arrange
    stream = Stream(id=uuid4(), camera_id=uuid4(), source_url="rtsp://test")
    await repository.save(stream)
    
    # Act
    await repository.delete(stream.id)
    found = await repository.find_by_id(stream.id)
    
    # Assert
    assert found is None
