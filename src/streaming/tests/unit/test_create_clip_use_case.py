"""Tests for CreateClipUseCase."""
import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from src.streaming.application.use_cases.create_clip import CreateClipUseCase
from src.streaming.application.dtos.create_clip_dto import CreateClipDTO
from src.streaming.domain.entities.recording import Recording
from src.streaming.domain.value_objects.retention_policy import RetentionPolicy
from src.streaming.infrastructure.persistence.clip_repository_impl import ClipRepositoryImpl
from src.streaming.infrastructure.persistence.recording_repository_impl import RecordingRepositoryImpl
from src.shared_kernel.infrastructure.message_broker import MessageBroker
from src.shared_kernel.domain.domain_exception import DomainException


@pytest.mark.asyncio
async def test_create_clip_success():
    """Test create clip success."""
    recording_id = uuid4()
    
    clip_repository = ClipRepositoryImpl()
    recording_repository = RecordingRepositoryImpl()
    message_broker = MessageBroker()
    
    recording = Recording(
        id=recording_id,
        stream_id=uuid4(),
        retention_policy=RetentionPolicy(7),
        storage_path="/recordings/test.mp4"
    )
    await recording_repository.save(recording)
    
    start_time = datetime.utcnow()
    end_time = start_time + timedelta(minutes=5)
    
    dto = CreateClipDTO(
        recording_id=recording_id,
        start_time=start_time,
        end_time=end_time
    )
    use_case = CreateClipUseCase(clip_repository, recording_repository, message_broker)
    
    result = await use_case.execute(dto)
    
    assert result.recording_id == recording_id
    assert result.status == "PENDING"
    assert result.duration_seconds == 300


@pytest.mark.asyncio
async def test_create_clip_recording_not_found():
    """Test create clip with recording not found."""
    clip_repository = ClipRepositoryImpl()
    recording_repository = RecordingRepositoryImpl()
    message_broker = MessageBroker()
    
    dto = CreateClipDTO(
        recording_id=uuid4(),
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(minutes=5)
    )
    use_case = CreateClipUseCase(clip_repository, recording_repository, message_broker)
    
    with pytest.raises(DomainException, match="Recording not found"):
        await use_case.execute(dto)
