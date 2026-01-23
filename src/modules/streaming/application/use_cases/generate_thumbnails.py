"""Generate thumbnails use case."""
from uuid import UUID
from typing import List
from src.shared.application.use_case import UseCase
from src.streaming.application.dtos.generate_thumbnails_dto import GenerateThumbnailsDTO
from src.streaming.application.dtos.thumbnail_response_dto import ThumbnailResponseDTO
from src.streaming.domain.repositories.recording_repository import RecordingRepository
from src.streaming.domain.services.thumbnail_service import ThumbnailService
from src.shared.domain.domain_exception import DomainException


class GenerateThumbnailsUseCase(UseCase[GenerateThumbnailsDTO, List[ThumbnailResponseDTO]]):
    """Generate thumbnails use case."""
    
    def __init__(
        self,
        recording_repository: RecordingRepository,
        thumbnail_service: ThumbnailService
    ):
        self.recording_repository = recording_repository
        self.thumbnail_service = thumbnail_service
    
    async def execute(self, dto: GenerateThumbnailsDTO) -> List[ThumbnailResponseDTO]:
        """Execute use case."""
        recording = await self.recording_repository.find_by_id(dto.recording_id)
        if not recording:
            raise DomainException("Recording not found")
        
        if not recording.storage_path:
            raise DomainException("Recording has no storage path")
        
        thumbnail_urls = await self.thumbnail_service.generate_thumbnails(
            video_path=recording.storage_path,
            start_time=recording.started_at,
            end_time=recording.stopped_at or recording.started_at,
            interval_seconds=dto.interval_seconds
        )
        
        return [
            ThumbnailResponseDTO(
                recording_id=recording.id,
                url=url,
                timestamp=recording.started_at
            )
            for url in thumbnail_urls
        ]
