"""Receive LPR event use case."""
from uuid import uuid4
from src.shared_kernel.application.use_case import UseCase
from src.ai.application.dtos.receive_lpr_event_dto import ReceiveLPREventDTO
from src.ai.application.dtos.lpr_event_response_dto import LPREventResponseDTO
from src.ai.domain.entities.lpr_event import LPREvent
from src.ai.domain.repositories.lpr_event_repository import LPREventRepository
from src.streaming.domain.services.storage_service import StorageService
from src.shared_kernel.infrastructure.observability import BusinessMetrics


class ReceiveLPREventUseCase(UseCase[ReceiveLPREventDTO, LPREventResponseDTO]):
    """Receive LPR event use case."""
    
    def __init__(
        self,
        lpr_event_repository: LPREventRepository,
        storage_service: StorageService
    ):
        self.lpr_event_repository = lpr_event_repository
        self.storage_service = storage_service
    
    async def execute(self, dto: ReceiveLPREventDTO) -> LPREventResponseDTO:
        """Execute use case."""
        image_url = None
        if dto.image_base64:
            import base64
            image_data = base64.b64decode(dto.image_base64)
            image_path = f"lpr/{dto.camera_id}/{uuid4()}.jpg"
            
            temp_file = f"/tmp/{uuid4()}.jpg"
            with open(temp_file, "wb") as f:
                f.write(image_data)
            
            image_url = await self.storage_service.upload_file(temp_file, image_path)
        
        event = LPREvent(
            id=uuid4(),
            camera_id=dto.camera_id,
            plate=dto.plate,
            confidence=dto.confidence,
            image_url=image_url,
            detected_at=dto.detected_at,
            city_id=dto.city_id
        )
        
        await self.lpr_event_repository.save(event)

        # Update metrics
        BusinessMetrics.increment_lpr_events()
        
        return LPREventResponseDTO(
            event_id=event.id,
            camera_id=event.camera_id,
            plate=event.plate,
            confidence=event.confidence,
            image_url=event.image_url,
            detected_at=event.detected_at,
            city_id=event.city_id
        )
