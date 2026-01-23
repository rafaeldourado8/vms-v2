"""Stop stream use case."""
from uuid import UUID
from src.shared.application.use_case import UseCase
from src.streaming.domain.repositories.stream_repository import StreamRepository
from src.streaming.domain.services.mediamtx_client import MediaMTXClient
from src.shared.domain.domain_exception import DomainException
from src.shared.infrastructure.observability import BusinessMetrics


class StopStreamUseCase(UseCase[UUID, None]):
    """Stop stream use case."""

    def __init__(
        self,
        stream_repository: StreamRepository,
        mediamtx_client: MediaMTXClient
    ):
        self.stream_repository = stream_repository
        self.mediamtx_client = mediamtx_client

    async def execute(self, stream_id: UUID) -> None:
        """Execute use case."""
        stream = await self.stream_repository.find_by_id(stream_id)
        if not stream:
            raise DomainException("Stream not found")

        if not stream.is_active():
            raise DomainException("Stream is not active")

        await self.mediamtx_client.stop_stream(str(stream.id))
        
        stream.stop()
        await self.stream_repository.save(stream)

        # Update metrics
        active_streams = await self.stream_repository.list_active()
        BusinessMetrics.update_active_streams(len(active_streams))
