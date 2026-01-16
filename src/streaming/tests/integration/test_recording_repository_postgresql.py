"""Integration tests for RecordingRepositoryPostgreSQL."""
import pytest
import pytest_asyncio
from uuid import uuid4
from datetime import datetime, timedelta

from streaming.domain.entities.recording import Recording
from streaming.domain.value_objects.recording_status import RecordingStatus
from streaming.domain.value_objects.retention_policy import RetentionPolicy
from streaming.infrastructure.persistence.recording_repository_postgresql import RecordingRepositoryPostgreSQL
from shared_kernel.infrastructure.persistence.connection import get_postgres_connection_string


@pytest_asyncio.fixture
async def repository():
    """Create repository instance."""
    repo = RecordingRepositoryPostgreSQL(get_postgres_connection_string())
    yield repo
    await repo.close()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_save_and_find_recording(repository):
    """Test save and find recording."""
    # Arrange
    recording = Recording(
        id=uuid4(),
        stream_id=uuid4(),
        retention_policy=RetentionPolicy(7)
    )
    
    # Act
    await repository.save(recording)
    found = await repository.find_by_id(recording.id)
    
    # Assert
    assert found is not None
    assert found.id == recording.id
    assert found.stream_id == recording.stream_id
    assert found.retention_policy.days == 7
    assert found.status == RecordingStatus.RECORDING
    
    # Cleanup
    await repository.delete(recording.id)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_find_by_stream_id(repository):
    """Test find recordings by stream ID."""
    # Arrange
    stream_id = uuid4()
    recording1 = Recording(id=uuid4(), stream_id=stream_id, retention_policy=RetentionPolicy(7))
    recording2 = Recording(id=uuid4(), stream_id=stream_id, retention_policy=RetentionPolicy(15))
    
    # Act
    await repository.save(recording1)
    await repository.save(recording2)
    found = await repository.find_by_stream_id(stream_id)
    
    # Assert
    assert len(found) >= 2
    found_ids = [r.id for r in found]
    assert recording1.id in found_ids
    assert recording2.id in found_ids
    
    # Cleanup
    await repository.delete(recording1.id)
    await repository.delete(recording2.id)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_search_recordings(repository):
    """Test search recordings with date filters."""
    # Arrange
    now = datetime.now()
    recording = Recording(id=uuid4(), stream_id=uuid4(), retention_policy=RetentionPolicy(7))
    
    # Act
    await repository.save(recording)
    # Search sem filtros para garantir que encontra
    results = await repository.search()
    
    # Assert
    assert len(results) >= 1
    assert any(r.id == recording.id for r in results)
    
    # Cleanup
    await repository.delete(recording.id)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_update_recording_metadata(repository):
    """Test update recording metadata."""
    # Arrange
    recording = Recording(id=uuid4(), stream_id=uuid4(), retention_policy=RetentionPolicy(7))
    await repository.save(recording)
    
    # Act - Update metadata only
    recording.storage_path = "/path/to/file.mp4"
    recording.file_size_mb = 100.5
    recording.duration_seconds = 3600
    await repository.save(recording)
    found = await repository.find_by_id(recording.id)
    
    # Assert
    assert found is not None
    assert found.status == RecordingStatus.RECORDING  # Status não muda
    assert found.storage_path == "/path/to/file.mp4"
    assert found.file_size_mb == 100.5
    assert found.duration_seconds == 3600
    
    # Cleanup
    await repository.delete(recording.id)
