"""FFmpeg service interface."""
from abc import ABC, abstractmethod
from uuid import UUID


class FFmpegService(ABC):
    """FFmpeg service interface."""
    
    @abstractmethod
    async def start_recording(self, recording_id: UUID, source_url: str, output_path: str) -> bool:
        """Start recording from RTSP source."""
        pass
    
    @abstractmethod
    async def stop_recording(self, recording_id: UUID) -> bool:
        """Stop recording."""
        pass
    
    @abstractmethod
    async def is_recording(self, recording_id: UUID) -> bool:
        """Check if recording is active."""
        pass
