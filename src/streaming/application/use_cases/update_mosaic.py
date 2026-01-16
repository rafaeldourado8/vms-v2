"""Update mosaic use case."""
from uuid import UUID
from src.shared_kernel.application.use_case import UseCase
from src.streaming.application.dtos.update_mosaic_dto import UpdateMosaicDTO
from src.streaming.application.dtos.mosaic_response_dto import MosaicResponseDTO
from src.streaming.domain.repositories.mosaic_repository import MosaicRepository
from src.shared_kernel.domain.domain_exception import DomainException


class UpdateMosaicUseCase(UseCase[UpdateMosaicDTO, MosaicResponseDTO]):
    """Update mosaic use case."""
    
    def __init__(self, mosaic_repository: MosaicRepository):
        self.mosaic_repository = mosaic_repository
    
    async def execute(self, dto: UpdateMosaicDTO) -> MosaicResponseDTO:
        """Execute use case."""
        mosaic = await self.mosaic_repository.find_by_id(dto.mosaic_id)
        if not mosaic:
            raise DomainException("Mosaic not found")
        
        if dto.name:
            mosaic.name = dto.name
        
        if dto.layout:
            mosaic.update_layout(dto.layout)
        
        if dto.camera_ids is not None:
            mosaic.camera_ids = dto.camera_ids
            mosaic._validate()
        
        await self.mosaic_repository.save(mosaic)
        
        return MosaicResponseDTO(
            mosaic_id=mosaic.id,
            user_id=mosaic.user_id,
            name=mosaic.name,
            layout=mosaic.layout,
            camera_ids=mosaic.camera_ids
        )
