"""LPR Event repository implementation."""
from uuid import UUID
from typing import List, Optional
from datetime import datetime
from src.ai.domain.entities.lpr_event import LPREvent
from src.ai.domain.repositories.lpr_event_repository import LPREventRepository


class LPREventRepositoryImpl(LPREventRepository):
    """In-memory LPR event repository implementation."""
    
    def __init__(self):
        self._events: dict[UUID, LPREvent] = {}
    
    async def save(self, entity: LPREvent) -> LPREvent:
        """Save event."""
        self._events[entity.id] = entity
        return entity
    
    async def find_by_id(self, id: UUID) -> Optional[LPREvent]:
        """Find event by ID."""
        return self._events.get(id)
    
    async def find_all(self) -> List[LPREvent]:
        """Find all events."""
        return list(self._events.values())
    
    async def delete(self, id: UUID) -> bool:
        """Delete event."""
        if id in self._events:
            del self._events[id]
            return True
        return False
    
    async def search(
        self,
        plate: Optional[str] = None,
        camera_id: Optional[UUID] = None,
        city_id: Optional[UUID] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[LPREvent]:
        """Search events by filters."""
        results = list(self._events.values())
        
        if plate:
            results = [e for e in results if plate.upper() in e.plate]
        
        if camera_id:
            results = [e for e in results if e.camera_id == camera_id]
        
        if city_id:
            results = [e for e in results if e.city_id == city_id]
        
        if start_date:
            results = [e for e in results if e.detected_at >= start_date]
        
        if end_date:
            results = [e for e in results if e.detected_at <= end_date]
        
        return sorted(results, key=lambda e: e.detected_at, reverse=True)
    
    async def find_by_plate(self, plate: str) -> List[LPREvent]:
        """Find events by plate."""
        return [e for e in self._events.values() if e.plate == plate.upper()]
