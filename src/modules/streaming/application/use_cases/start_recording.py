"""Start recording use case."""
from uuid import uuid4
from src.shared.application.use_case import UseCase
from src.streaming.application.dtos.start_recording_dto import StartRecordingDTO
from src.streaming.application.dtos.recording_response_dto import RecordingResponseDTO
from src.streaming.domain.entities.recording import Recording
from src.streaming.domain.value_objects.retention_policy import RetentionPolicy
from src.streaming.domain.repositories.recording_repository import RecordingRepository
from src.streaming.domain.repositories.stream_repository import StreamRepository
from src.shared.domain.domain_exception import DomainException
from src.shared.infrastructure.message_broker import MessageBroker
from src.shared.infrastructure.observability import BusinessMetrics


class StartRecordingUseCase(UseCase[StartRecordingDTO, RecordingResponseDTO]):
    """Start recording use case."""
    
    def __init__(
        self,
        recording_repository: RecordingRepository,
        stream_repository: StreamRepository,
        message_broker: MessageBroker
    ):
        self.recording_repository = recording_repository
        self.stream_repository = stream_repository
        self.message_broker = message_broker
    
    async def execute(self, dto: StartRecordingDTO) -> RecordingResponseDTO:
        """Execute use case."""
        stream = await self.stream_repository.find_by_id(dto.stream_id)
        if not stream:
            raise DomainException("Stream not found")
        
        if not stream.is_active():
            raise DomainException("Stream is not active")
        
        active_recording = await self.recording_repository.find_active_by_stream_id(dto.stream_id)
        if active_recording:
            raise DomainException("Recording already active for this stream")
        
        retention_policy = RetentionPolicy(dto.retention_days)
        recording = Recording(
            id=uuid4(),
            stream_id=dto.stream_id,
            retention_policy=retention_policy
        )
        
        await self.recording_repository.save(recording)
        
        await self.message_broker.publish(
            exchange="recordings",
            routing_key="recording.start",
            message={
                "recording_id": str(recording.id),
                "stream_id": str(recording.stream_id),
                "source_url": stream.source_url
            }
        )

        # Update metrics
        active_recordings = await self.recording_repository.count_active()
        BusinessMetrics.update_active_recordings(active_recordings)
        
        return RecordingResponseDTO(
            recording_id=recording.id,
            stream_id=recording.stream_id,
            status=recording.status.value,
            started_at=recording.started_at,
            stopped_at=recording.stopped_at,
            retention_days=recording.retention_policy.days,
            storage_path=recording.storage_path,
            file_size_mb=recording.file_size_mb,
            duration_seconds=recording.duration_seconds
        )
