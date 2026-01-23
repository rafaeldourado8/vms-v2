"""Start stream use case."""
from uuid import uuid4
from src.shared.application.use_case import UseCase
from src.streaming.application.dtos.start_stream_dto import StartStreamDTO
from src.streaming.application.dtos.stream_response_dto import StreamResponseDTO
from src.streaming.domain.entities.stream import Stream
from src.streaming.domain.value_objects.stream_status import StreamStatus
from src.streaming.domain.repositories.stream_repository import StreamRepository
from src.streaming.domain.services.mediamtx_client import MediaMTXClient
from src.shared.domain.domain_exception import DomainException
from src.shared.infrastructure.observability import BusinessMetrics


class StartStreamUseCase(UseCase[StartStreamDTO, StreamResponseDTO]):
    """Start stream use case."""

    def __init__(
        self,
        stream_repository: StreamRepository,
        mediamtx_client: MediaMTXClient
    ):
        self.stream_repository = stream_repository
        self.mediamtx_client = mediamtx_client

    async def execute(self, input_dto: StartStreamDTO) -> StreamResponseDTO:
        """Execute use case."""
        existing = await self.stream_repository.find_by_camera_id(input_dto.camera_id)
        if existing and existing.is_active():
            raise DomainException("Stream already active for this camera")

        stream = Stream(
            id=uuid4(),
            camera_id=input_dto.camera_id,
            source_url=input_dto.source_url,
            status=StreamStatus.STOPPED
        )

        stream.start()
        
        success = await self.mediamtx_client.start_stream(
            str(stream.id),
            stream.source_url
        )

        if success:
            stream.mark_running()
        else:
            stream.mark_error()
            raise DomainException("Failed to start stream in MediaMTX")

        await self.stream_repository.save(stream)

        # Update metrics
        active_streams = await self.stream_repository.list_active()
        BusinessMetrics.update_active_streams(len(active_streams))

        return StreamResponseDTO(
            id=stream.id,
            camera_id=stream.camera_id,
            source_url=stream.source_url,
            status=stream.status.value,
            started_at=stream.started_at,
            stopped_at=stream.stopped_at
        )
