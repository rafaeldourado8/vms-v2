"""Create mosaic use case."""
from uuid import uuid4
from src.shared_kernel.application.use_case import UseCase
from src.streaming.application.dtos.create_mosaic_dto import CreateMosaicDTO
from src.streaming.application.dtos.mosaic_response_dto import MosaicResponseDTO
from src.streaming.domain.entities.mosaic import Mosaic
from src.streaming.domain.repositories.mosaic_repository import MosaicRepository


class CreateMosaicUseCase(UseCase[CreateMosaicDTO, MosaicResponseDTO]):
    """Create mosaic use case."""
    
    def __init__(self, mosaic_repository: MosaicRepository):
        self.mosaic_repository = mosaic_repository
    
    async def execute(self, dto: CreateMosaicDTO) -> MosaicResponseDTO:
        """Execute use case."""
        mosaic = Mosaic(
            id=uuid4(),
            user_id=dto.user_id,
            name=dto.name,
            layout=dto.layout,
            camera_ids=dto.camera_ids
        )
        
        await self.mosaic_repository.save(mosaic)
        
        return MosaicResponseDTO(
            mosaic_id=mosaic.id,
            user_id=mosaic.user_id,
            name=mosaic.name,
            layout=mosaic.layout,
            camera_ids=mosaic.camera_ids
        )
