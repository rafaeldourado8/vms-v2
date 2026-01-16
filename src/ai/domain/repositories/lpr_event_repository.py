"""LPR Event repository interface."""
from abc import abstractmethod
from uuid import UUID
from typing import List, Optional
from datetime import datetime
from src.shared_kernel.domain.repository import Repository
from src.ai.domain.entities.lpr_event import LPREvent


class LPREventRepository(Repository[LPREvent]):
    """LPR Event repository interface."""
    
    @abstractmethod
    async def search(
        self,
        plate: Optional[str] = None,
        camera_id: Optional[UUID] = None,
        city_id: Optional[UUID] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[LPREvent]:
        """Search LPR events by filters."""
        pass
    
    @abstractmethod
    async def find_by_plate(self, plate: str) -> List[LPREvent]:
        """Find events by plate."""
        pass
