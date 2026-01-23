"""Tests for GetTimelineUseCase."""
import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from src.streaming.application.use_cases.get_timeline import GetTimelineUseCase
from src.streaming.application.dtos.get_timeline_dto import GetTimelineDTO
from src.streaming.domain.entities.recording import Recording
from src.streaming.domain.value_objects.retention_policy import RetentionPolicy
from src.streaming.infrastructure.persistence.recording_repository_impl import RecordingRepositoryImpl
from src.shared.domain.domain_exception import DomainException


@pytest.mark.asyncio
async def test_get_timeline_success():
    """Test get timeline success."""
    stream_id = uuid4()
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(hours=2)
    
    recording_repository = RecordingRepositoryImpl()
    
    recording = Recording(
        id=uuid4(),
        stream_id=stream_id,
        retention_policy=RetentionPolicy(7),
        started_at=start_date,
        stopped_at=start_date + timedelta(hours=1)
    )
    await recording_repository.save(recording)
    
    dto = GetTimelineDTO(stream_id=stream_id, start_date=start_date, end_date=end_date)
    use_case = GetTimelineUseCase(recording_repository)
    
    result = await use_case.execute(dto)
    
    assert result.stream_id == stream_id
    assert len(result.segments) == 1
    assert result.total_duration_seconds > 0


@pytest.mark.asyncio
async def test_get_timeline_no_recordings():
    """Test get timeline with no recordings."""
    recording_repository = RecordingRepositoryImpl()
    
    dto = GetTimelineDTO(
        stream_id=uuid4(),
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(hours=2)
    )
    use_case = GetTimelineUseCase(recording_repository)
    
    with pytest.raises(DomainException, match="No recordings found"):
        await use_case.execute(dto)
