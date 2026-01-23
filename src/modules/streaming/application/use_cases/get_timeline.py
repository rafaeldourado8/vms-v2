"""Get timeline use case."""
from uuid import UUID, uuid4
from datetime import datetime
from src.shared.application.use_case import UseCase
from src.streaming.application.dtos.get_timeline_dto import GetTimelineDTO
from src.streaming.application.dtos.timeline_response_dto import TimelineResponseDTO
from src.streaming.domain.entities.timeline import Timeline
from src.streaming.domain.value_objects.timeline_segment import TimelineSegment
from src.streaming.domain.repositories.recording_repository import RecordingRepository
from src.shared.domain.domain_exception import DomainException


class GetTimelineUseCase(UseCase[GetTimelineDTO, TimelineResponseDTO]):
    """Get timeline use case."""
    
    def __init__(self, recording_repository: RecordingRepository):
        self.recording_repository = recording_repository
    
    async def execute(self, dto: GetTimelineDTO) -> TimelineResponseDTO:
        """Execute use case."""
        recordings = await self.recording_repository.search(
            stream_id=dto.stream_id,
            start_date=dto.start_date,
            end_date=dto.end_date
        )
        
        if not recordings:
            raise DomainException("No recordings found for this period")
        
        timeline = Timeline(
            id=uuid4(),
            stream_id=dto.stream_id,
            start_date=dto.start_date,
            end_date=dto.end_date
        )
        
        for recording in recordings:
            segment = TimelineSegment(
                start_time=recording.started_at,
                end_time=recording.stopped_at or datetime.utcnow(),
                has_recording=True
            )
            timeline.add_segment(segment)
        
        return TimelineResponseDTO(
            timeline_id=timeline.id,
            stream_id=timeline.stream_id,
            start_date=timeline.start_date,
            end_date=timeline.end_date,
            segments=[
                {
                    "start_time": s.start_time,
                    "end_time": s.end_time,
                    "has_recording": s.has_recording,
                    "duration_seconds": s.duration_seconds
                }
                for s in timeline.segments
            ],
            total_duration_seconds=timeline.get_total_duration(),
            has_gaps=timeline.has_gaps()
        )
