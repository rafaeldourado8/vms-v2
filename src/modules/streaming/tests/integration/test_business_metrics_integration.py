"""Test business metrics integration in use cases."""
import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4
from datetime import datetime

from src.streaming.application.use_cases.start_stream import StartStreamUseCase
from src.streaming.application.use_cases.stop_stream import StopStreamUseCase
from src.streaming.application.use_cases.start_recording import StartRecordingUseCase
from src.streaming.application.use_cases.stop_recording import StopRecordingUseCase
from src.ai.application.use_cases.receive_lpr_event import ReceiveLPREventUseCase
from src.streaming.application.dtos.start_stream_dto import StartStreamDTO
from src.streaming.application.dtos.start_recording_dto import StartRecordingDTO
from src.ai.application.dtos.receive_lpr_event_dto import ReceiveLPREventDTO


@pytest.mark.asyncio
@patch('src.shared_kernel.infrastructure.observability.business_metrics.BusinessMetrics.update_active_streams')
async def test_start_stream_updates_metrics(mock_update):
    """Test StartStreamUseCase updates active streams metric."""
    stream_repo = AsyncMock()
    mediamtx_client = AsyncMock()
    
    stream_repo.find_by_camera_id.return_value = None
    mediamtx_client.start_stream.return_value = True
    stream_repo.list_active.return_value = [AsyncMock(), AsyncMock()]
    
    use_case = StartStreamUseCase(stream_repo, mediamtx_client)
    dto = StartStreamDTO(camera_id=uuid4(), source_url="rtsp://test")
    
    await use_case.execute(dto)
    
    mock_update.assert_called_once_with(2)


@pytest.mark.asyncio
@patch('src.shared_kernel.infrastructure.observability.business_metrics.BusinessMetrics.update_active_streams')
async def test_stop_stream_updates_metrics(mock_update):
    """Test StopStreamUseCase updates active streams metric."""
    stream_repo = AsyncMock()
    mediamtx_client = AsyncMock()
    
    stream = AsyncMock()
    stream.is_active.return_value = True
    stream_repo.find_by_id.return_value = stream
    stream_repo.list_active.return_value = [AsyncMock()]
    
    use_case = StopStreamUseCase(stream_repo, mediamtx_client)
    
    await use_case.execute(uuid4())
    
    mock_update.assert_called_once_with(1)


@pytest.mark.asyncio
@patch('src.shared_kernel.infrastructure.observability.business_metrics.BusinessMetrics.update_active_recordings')
async def test_start_recording_updates_metrics(mock_update):
    """Test StartRecordingUseCase updates active recordings metric."""
    recording_repo = AsyncMock()
    stream_repo = AsyncMock()
    message_broker = AsyncMock()
    
    stream = AsyncMock()
    stream.is_active.return_value = True
    stream.source_url = "rtsp://test"
    stream_repo.find_by_id.return_value = stream
    recording_repo.find_active_by_stream_id.return_value = None
    recording_repo.count_active.return_value = 3
    
    use_case = StartRecordingUseCase(recording_repo, stream_repo, message_broker)
    dto = StartRecordingDTO(stream_id=uuid4(), retention_days=7)
    
    await use_case.execute(dto)
    
    mock_update.assert_called_once_with(3)


@pytest.mark.asyncio
@patch('src.shared_kernel.infrastructure.observability.business_metrics.BusinessMetrics.update_active_recordings')
async def test_stop_recording_updates_metrics(mock_update):
    """Test StopRecordingUseCase updates active recordings metric."""
    recording_repo = AsyncMock()
    message_broker = AsyncMock()
    
    recording = AsyncMock()
    recording.is_active.return_value = True
    recording_repo.find_by_id.return_value = recording
    recording_repo.count_active.return_value = 1
    
    use_case = StopRecordingUseCase(recording_repo, message_broker)
    
    await use_case.execute(uuid4())
    
    mock_update.assert_called_once_with(1)


@pytest.mark.asyncio
@patch('src.shared_kernel.infrastructure.observability.business_metrics.BusinessMetrics.increment_lpr_events')
async def test_receive_lpr_event_updates_metrics(mock_increment):
    """Test ReceiveLPREventUseCase increments LPR events counter."""
    lpr_repo = AsyncMock()
    storage_service = AsyncMock()
    
    use_case = ReceiveLPREventUseCase(lpr_repo, storage_service)
    dto = ReceiveLPREventDTO(
        camera_id=uuid4(),
        plate="ABC1234",
        confidence=0.95,
        detected_at=datetime.now(),
        city_id=uuid4()
    )
    
    await use_case.execute(dto)
    
    mock_increment.assert_called_once()
