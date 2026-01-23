"""Unit tests for StartStreamUseCase."""
import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, Mock
from src.streaming.application.use_cases.start_stream import StartStreamUseCase
from src.streaming.application.dtos.start_stream_dto import StartStreamDTO
from src.shared.domain.domain_exception import DomainException


@pytest.mark.unit
class TestStartStreamUseCase:
    """StartStreamUseCase tests."""

    @pytest.mark.asyncio
    async def test_start_stream_success(self):
        """Test start stream successfully."""
        repository = Mock()
        repository.find_by_camera_id = AsyncMock(return_value=None)
        repository.save = AsyncMock()
        
        mediamtx = Mock()
        mediamtx.start_stream = AsyncMock(return_value=True)
        
        use_case = StartStreamUseCase(repository, mediamtx)
        dto = StartStreamDTO(
            camera_id=uuid4(),
            source_url="rtsp://192.168.1.100:554/stream"
        )
        
        result = await use_case.execute(dto)
        
        assert result.status == "RUNNING"
        assert repository.save.called

    @pytest.mark.asyncio
    async def test_start_stream_already_active(self):
        """Test start stream when already active."""
        from src.streaming.domain.entities.stream import Stream
        from src.streaming.domain.value_objects.stream_status import StreamStatus
        
        active_stream = Stream(
            id=uuid4(),
            camera_id=uuid4(),
            source_url="rtsp://test",
            status=StreamStatus.RUNNING
        )
        
        repository = Mock()
        repository.find_by_camera_id = AsyncMock(return_value=active_stream)
        
        mediamtx = Mock()
        
        use_case = StartStreamUseCase(repository, mediamtx)
        dto = StartStreamDTO(
            camera_id=active_stream.camera_id,
            source_url="rtsp://192.168.1.100:554/stream"
        )
        
        with pytest.raises(DomainException, match="already active"):
            await use_case.execute(dto)

    @pytest.mark.asyncio
    async def test_start_stream_mediamtx_failure(self):
        """Test start stream when MediaMTX fails."""
        repository = Mock()
        repository.find_by_camera_id = AsyncMock(return_value=None)
        
        mediamtx = Mock()
        mediamtx.start_stream = AsyncMock(return_value=False)
        
        use_case = StartStreamUseCase(repository, mediamtx)
        dto = StartStreamDTO(
            camera_id=uuid4(),
            source_url="rtsp://192.168.1.100:554/stream"
        )
        
        with pytest.raises(DomainException, match="Failed to start"):
            await use_case.execute(dto)
