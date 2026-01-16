"""Search LPR events use case."""
from typing import List
from src.shared_kernel.application.use_case import UseCase
from src.ai.application.dtos.search_lpr_events_dto import SearchLPREventsDTO
from src.ai.application.dtos.lpr_event_response_dto import LPREventResponseDTO
from src.ai.domain.repositories.lpr_event_repository import LPREventRepository


class SearchLPREventsUseCase(UseCase[SearchLPREventsDTO, List[LPREventResponseDTO]]:
    """Search LPR events use case."""
    
    def __init__(self, lpr_event_repository: LPREventRepository):
        self.lpr_event_repository = lpr_event_repository
    
    async def execute(self, dto: SearchLPREventsDTO) -> List[LPREventResponseDTO]:
        """Execute use case."""
        events = await self.lpr_event_repository.search(
            plate=dto.plate,
            camera_id=dto.camera_id,
            city_id=dto.city_id,
            start_date=dto.start_date,
            end_date=dto.end_date
        )
        
        return [
            LPREventResponseDTO(
                event_id=e.id,
                camera_id=e.camera_id,
                plate=e.plate,
                confidence=e.confidence,
                image_url=e.image_url,
                detected_at=e.detected_at,
                city_id=e.city_id
            )
            for e in events
        ]
