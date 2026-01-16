"""Search recordings use case."""
from typing import List
from src.shared_kernel.application.use_case import UseCase
from src.streaming.application.dtos.search_recordings_dto import SearchRecordingsDTO
from src.streaming.application.dtos.recording_response_dto import RecordingResponseDTO
from src.streaming.domain.repositories.recording_repository import RecordingRepository


class SearchRecordingsUseCase(UseCase[SearchRecordingsDTO, List[RecordingResponseDTO]]):
    """Search recordings use case."""
    
    def __init__(self, recording_repository: RecordingRepository):
        self.recording_repository = recording_repository
    
    async def execute(self, dto: SearchRecordingsDTO) -> List[RecordingResponseDTO]:
        """Execute use case."""
        recordings = await self.recording_repository.search(
            stream_id=dto.stream_id,
            start_date=dto.start_date,
            end_date=dto.end_date
        )
        
        return [
            RecordingResponseDTO(
                recording_id=r.id,
                stream_id=r.stream_id,
                status=r.status.value,
                started_at=r.started_at,
                stopped_at=r.stopped_at,
                retention_days=r.retention_policy.days,
                storage_path=r.storage_path,
                file_size_mb=r.file_size_mb,
                duration_seconds=r.duration_seconds
            )
            for r in recordings
        ]
