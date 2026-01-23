"""Create clip use case."""
from uuid import uuid4
from src.shared.application.use_case import UseCase
from src.streaming.application.dtos.create_clip_dto import CreateClipDTO
from src.streaming.application.dtos.clip_response_dto import ClipResponseDTO
from src.streaming.domain.entities.clip import Clip
from src.streaming.domain.repositories.clip_repository import ClipRepository
from src.streaming.domain.repositories.recording_repository import RecordingRepository
from src.shared.domain.domain_exception import DomainException
from src.shared.infrastructure.message_broker import MessageBroker


class CreateClipUseCase(UseCase[CreateClipDTO, ClipResponseDTO]):
    """Create clip use case."""
    
    def __init__(
        self,
        clip_repository: ClipRepository,
        recording_repository: RecordingRepository,
        message_broker: MessageBroker
    ):
        self.clip_repository = clip_repository
        self.recording_repository = recording_repository
        self.message_broker = message_broker
    
    async def execute(self, dto: CreateClipDTO) -> ClipResponseDTO:
        """Execute use case."""
        recording = await self.recording_repository.find_by_id(dto.recording_id)
        if not recording:
            raise DomainException("Recording not found")
        
        if not recording.storage_path:
            raise DomainException("Recording has no storage path")
        
        clip = Clip(
            id=uuid4(),
            recording_id=dto.recording_id,
            start_time=dto.start_time,
            end_time=dto.end_time
        )
        
        await self.clip_repository.save(clip)
        
        await self.message_broker.publish(
            exchange="clips",
            routing_key="clip.create",
            message={
                "clip_id": str(clip.id),
                "recording_id": str(clip.recording_id),
                "start_time": clip.start_time.isoformat(),
                "end_time": clip.end_time.isoformat(),
                "source_path": recording.storage_path
            }
        )
        
        return ClipResponseDTO(
            clip_id=clip.id,
            recording_id=clip.recording_id,
            start_time=clip.start_time,
            end_time=clip.end_time,
            status=clip.status.value,
            storage_path=clip.storage_path,
            file_size_mb=clip.file_size_mb,
            duration_seconds=clip.duration_seconds,
            created_at=clip.created_at
        )
