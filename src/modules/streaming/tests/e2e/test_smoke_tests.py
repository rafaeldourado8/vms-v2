"""Smoke tests for Sprint 11 infrastructure integration."""
import pytest
import pytest_asyncio
from uuid import uuid4
import tempfile
import os

from shared_kernel.infrastructure.persistence.connection import get_postgres_connection_string
from shared_kernel.infrastructure.rabbitmq_connection import get_rabbitmq_url
from shared_kernel.infrastructure.message_broker import MessageBrokerConfig
from streaming.infrastructure.persistence.stream_repository_postgresql import StreamRepositoryPostgreSQL
from streaming.infrastructure.persistence.recording_repository_postgresql import RecordingRepositoryPostgreSQL
from streaming.infrastructure.external_services.storage_service_impl import MinIOStorageService
from streaming.domain.entities.stream import Stream
from streaming.domain.entities.recording import Recording
from streaming.domain.value_objects.retention_policy import RetentionPolicy


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_smoke_postgresql_connection():
    """Smoke test: PostgreSQL connection works."""
    repo = StreamRepositoryPostgreSQL(get_postgres_connection_string())
    
    # Create and save a stream
    stream = Stream(
        id=uuid4(),
        camera_id=uuid4(),
        source_url="rtsp://test/smoke"
    )
    
    await repo.save(stream)
    found = await repo.find_by_id(stream.id)
    
    assert found is not None
    assert found.id == stream.id
    
    await repo.delete(stream.id)
    await repo.close()


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_smoke_rabbitmq_connection():
    """Smoke test: RabbitMQ connection works."""
    broker = MessageBrokerConfig(get_rabbitmq_url(), max_retries=1)
    await broker.connect()
    
    assert broker.connection is not None
    assert not broker.connection.is_closed
    
    await broker.close()


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_smoke_minio_connection():
    """Smoke test: MinIO connection works."""
    storage = MinIOStorageService()
    
    # Create temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Smoke test")
        temp_file = f.name
    
    try:
        remote_path = f"smoke/{uuid4()}.txt"
        
        # Upload
        result = await storage.upload_file(temp_file, remote_path)
        assert result.startswith("s3://")
        
        # Verify exists
        exists = await storage.file_exists(remote_path)
        assert exists is True
        
        # Cleanup
        await storage.delete_file(remote_path)
    finally:
        os.unlink(temp_file)


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_smoke_full_stack_stream_to_recording():
    """Smoke test: Full stack - Stream + Recording + PostgreSQL."""
    stream_repo = StreamRepositoryPostgreSQL(get_postgres_connection_string())
    recording_repo = RecordingRepositoryPostgreSQL(get_postgres_connection_string())
    
    try:
        # Create stream
        stream = Stream(
            id=uuid4(),
            camera_id=uuid4(),
            source_url="rtsp://test/fullstack"
        )
        stream.start()
        stream.mark_running()
        
        await stream_repo.save(stream)
        
        # Create recording for stream
        recording = Recording(
            id=uuid4(),
            stream_id=stream.id,
            retention_policy=RetentionPolicy(7)  # 7 days
        )
        
        await recording_repo.save(recording)
        
        # Verify both exist
        found_stream = await stream_repo.find_by_id(stream.id)
        found_recording = await recording_repo.find_by_id(recording.id)
        
        assert found_stream is not None
        assert found_recording is not None
        assert found_recording.stream_id == stream.id
        
        # Cleanup
        await recording_repo.delete(recording.id)
        await stream_repo.delete(stream.id)
    finally:
        await stream_repo.close()
        await recording_repo.close()


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_smoke_all_services_healthy():
    """Smoke test: All services (PostgreSQL, RabbitMQ, MinIO) are healthy."""
    errors = []
    
    # Test PostgreSQL
    try:
        repo = StreamRepositoryPostgreSQL(get_postgres_connection_string())
        await repo.find_all()
        await repo.close()
    except Exception as e:
        errors.append(f"PostgreSQL: {e}")
    
    # Test RabbitMQ
    try:
        broker = MessageBrokerConfig(get_rabbitmq_url())
        await broker.connect()
        await broker.close()
    except Exception as e:
        errors.append(f"RabbitMQ: {e}")
    
    # Test MinIO
    try:
        storage = MinIOStorageService()
        await storage.file_exists("health-check")
    except Exception as e:
        errors.append(f"MinIO: {e}")
    
    assert len(errors) == 0, f"Services unhealthy: {errors}"
