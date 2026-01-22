"""Thumbnail service interface."""
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime


class ThumbnailService(ABC):
    """Thumbnail service interface."""
    
    @abstractmethod
    async def generate_thumbnail(self, video_path: str, timestamp: datetime, output_path: str) -> str:
        """Generate single thumbnail from video."""
        pass
    
    @abstractmethod
    async def generate_thumbnails(
        self,
        video_path: str,
        start_time: datetime,
        end_time: datetime,
        interval_seconds: int = 60
    ) -> List[str]:
        """Generate multiple thumbnails at intervals."""
        pass
