"""Tests for StartRecordingUseCase."""
import pytest
from uuid import uuid4
from src.streaming.application.use_cases.start_recording import StartRecordingUseCase
from src.streaming.application.dtos.start_recording_dto import StartRecordingDTO
from src.streaming.domain.entities.stream import Stream
from src.streaming.domain.value_objects.stream_status import StreamStatus
from src.streaming.infrastructure.persistence.recording_repository_impl import RecordingRepositoryImpl
from src.streaming.infrastructure.persistence.stream_repository_impl import StreamRepositoryImpl
from src.shared.infrastructure.message_broker import MessageBroker
from src.shared.domain.domain_exception import DomainException


@pytest.mark.asyncio
async def test_start_recording_success():
    """Test start recording success."""
    stream_id = uuid4()
    camera_id = uuid4()
    
    stream_repository = StreamRepositoryImpl()
    recording_repository = RecordingRepositoryImpl()
    message_broker = MessageBroker()
    
    stream = Stream(
        id=stream_id,
        camera_id=camera_id,
        source_url="rtsp://camera",
        status=StreamStatus.RUNNING
    )
    await stream_repository.save(stream)
    
    dto = StartRecordingDTO(stream_id=stream_id, retention_days=7)
    use_case = StartRecordingUseCase(recording_repository, stream_repository, message_broker)
    
    result = await use_case.execute(dto)
    
    assert result.stream_id == stream_id
    assert result.status == "RECORDING"
    assert result.retention_days == 7


@pytest.mark.asyncio
async def test_start_recording_stream_not_found():
    """Test start recording with stream not found."""
    stream_repository = StreamRepositoryImpl()
    recording_repository = RecordingRepositoryImpl()
    message_broker = MessageBroker()
    
    dto = StartRecordingDTO(stream_id=uuid4(), retention_days=7)
    use_case = StartRecordingUseCase(recording_repository, stream_repository, message_broker)
    
    with pytest.raises(DomainException, match="Stream not found"):
        await use_case.execute(dto)


@pytest.mark.asyncio
async def test_start_recording_stream_not_active():
    """Test start recording with inactive stream."""
    stream_id = uuid4()
    
    stream_repository = StreamRepositoryImpl()
    recording_repository = RecordingRepositoryImpl()
    message_broker = MessageBroker()
    
    stream = Stream(
        id=stream_id,
        camera_id=uuid4(),
        source_url="rtsp://camera",
        status=StreamStatus.STOPPED
    )
    await stream_repository.save(stream)
    
    dto = StartRecordingDTO(stream_id=stream_id, retention_days=7)
    use_case = StartRecordingUseCase(recording_repository, stream_repository, message_broker)
    
    with pytest.raises(DomainException, match="Stream is not active"):
        await use_case.execute(dto)
