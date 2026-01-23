"""Stop recording use case."""
from uuid import UUID
from src.shared.application.use_case import UseCase
from src.streaming.domain.repositories.recording_repository import RecordingRepository
from src.shared.domain.domain_exception import DomainException
from src.shared.infrastructure.message_broker import MessageBroker
from src.shared.infrastructure.observability import BusinessMetrics


class StopRecordingUseCase(UseCase[UUID, None]):
    """Stop recording use case."""
    
    def __init__(
        self,
        recording_repository: RecordingRepository,
        message_broker: MessageBroker
    ):
        self.recording_repository = recording_repository
        self.message_broker = message_broker
    
    async def execute(self, recording_id: UUID) -> None:
        """Execute use case."""
        recording = await self.recording_repository.find_by_id(recording_id)
        if not recording:
            raise DomainException("Recording not found")
        
        if not recording.is_active():
            raise DomainException("Recording is not active")
        
        recording.stop()
        await self.recording_repository.save(recording)
        
        await self.message_broker.publish(
            exchange="recordings",
            routing_key="recording.stop",
            message={"recording_id": str(recording_id)}
        )

        # Update metrics
        active_recordings = await self.recording_repository.count_active()
        BusinessMetrics.update_active_recordings(active_recordings)
