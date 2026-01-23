"""Recording repository interface."""
from abc import abstractmethod
from uuid import UUID
from typing import List, Optional
from datetime import datetime
from src.shared.domain.repository import Repository
from src.streaming.domain.entities.recording import Recording


class RecordingRepository(Repository[Recording]):
    """Recording repository interface."""
    
    @abstractmethod
    async def find_by_stream_id(self, stream_id: UUID) -> List[Recording]:
        """Find recordings by stream ID."""
        pass
    
    @abstractmethod
    async def find_active_by_stream_id(self, stream_id: UUID) -> Optional[Recording]:
        """Find active recording by stream ID."""
        pass
    
    @abstractmethod
    async def search(
        self,
        stream_id: Optional[UUID] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Recording]:
        """Search recordings by filters."""
        pass
    
    @abstractmethod
    async def find_expired(self) -> List[Recording]:
        """Find recordings that should be deleted."""
        pass

    @abstractmethod
    async def count_active(self) -> int:
        """Count active recordings."""
        pass
