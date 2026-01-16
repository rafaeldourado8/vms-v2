"""LPR Event entity."""
from uuid import UUID
from datetime import datetime
from src.shared_kernel.domain.entity import Entity


class LPREvent(Entity):
    """LPR (License Plate Recognition) Event entity."""
    
    def __init__(
        self,
        id: UUID,
        camera_id: UUID,
        plate: str,
        confidence: float,
        image_url: str = None,
        detected_at: datetime = None,
        city_id: UUID = None
    ):
        super().__init__(id)
        self.camera_id = camera_id
        self.plate = plate.upper()
        self.confidence = confidence
        self.image_url = image_url
        self.detected_at = detected_at or datetime.utcnow()
        self.city_id = city_id
    
    def is_high_confidence(self) -> bool:
        """Check if detection has high confidence."""
        return self.confidence >= 0.8
