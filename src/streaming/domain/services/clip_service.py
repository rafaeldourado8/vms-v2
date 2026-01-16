"""Clip service interface."""
from abc import ABC, abstractmethod
from datetime import datetime


class ClipService(ABC):
    """Clip service interface."""
    
    @abstractmethod
    async def create_clip(
        self,
        source_path: str,
        output_path: str,
        start_time: datetime,
        end_time: datetime
    ) -> bool:
        """Create clip from video."""
        pass
