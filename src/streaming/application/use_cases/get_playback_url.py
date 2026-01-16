"""Get playback URL use case."""
from uuid import UUID
from src.shared_kernel.application.use_case import UseCase
from src.streaming.application.dtos.playback_url_response_dto import PlaybackUrlResponseDTO
from src.streaming.domain.repositories.recording_repository import RecordingRepository
from src.streaming.domain.services.storage_service import StorageService
from src.shared_kernel.domain.domain_exception import DomainException


class GetPlaybackUrlUseCase(UseCase[UUID, PlaybackUrlResponseDTO]):
    """Get playback URL use case."""
    
    def __init__(
        self,
        recording_repository: RecordingRepository,
        storage_service: StorageService
    ):
        self.recording_repository = recording_repository
        self.storage_service = storage_service
    
    async def execute(self, recording_id: UUID) -> PlaybackUrlResponseDTO:
        """Execute use case."""
        recording = await self.recording_repository.find_by_id(recording_id)
        if not recording:
            raise DomainException("Recording not found")
        
        if not recording.storage_path:
            raise DomainException("Recording has no storage path")
        
        playback_url = await self.storage_service.get_file_url(
            recording.storage_path,
            expires_in=3600
        )
        
        if not playback_url:
            raise DomainException("Failed to generate playback URL")
        
        return PlaybackUrlResponseDTO(
            recording_id=recording.id,
            playback_url=playback_url,
            expires_in=3600
        )
