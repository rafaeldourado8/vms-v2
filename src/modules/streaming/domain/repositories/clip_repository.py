"""Clip repository interface."""
from abc import abstractmethod
from uuid import UUID
from typing import List, Optional
from src.shared.domain.repository import Repository
from src.streaming.domain.entities.clip import Clip


class ClipRepository(Repository[Clip]):
    """Clip repository interface."""
    
    @abstractmethod
    async def find_by_recording_id(self, recording_id: UUID) -> List[Clip]:
        """Find clips by recording ID."""
        pass
    
    @abstractmethod
    async def find_pending(self) -> List[Clip]:
        """Find pending clips for processing."""
        pass
