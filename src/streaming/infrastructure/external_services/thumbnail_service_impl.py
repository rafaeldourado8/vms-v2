"""Thumbnail service implementation using FFmpeg."""
import os
import asyncio
from typing import List
from datetime import datetime, timedelta
from src.streaming.domain.services.thumbnail_service import ThumbnailService
from src.shared_kernel.infrastructure.logger import Logger


class ThumbnailServiceImpl(ThumbnailService):
    """Thumbnail service implementation."""
    
    def __init__(self):
        self.logger = Logger(__name__)
        self.output_dir = "/thumbnails"
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def generate_thumbnail(self, video_path: str, timestamp: datetime, output_path: str) -> str:
        """Generate single thumbnail from video."""
        try:
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-ss", timestamp.strftime("%H:%M:%S"),
                "-vframes", "1",
                "-vf", "scale=160:90",
                "-y",
                output_path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await process.wait()
            
            if process.returncode == 0:
                self.logger.info(f"Thumbnail generated: {output_path}")
                return output_path
            else:
                self.logger.error(f"Failed to generate thumbnail: {process.returncode}")
                return ""
                
        except Exception as e:
            self.logger.error(f"Error generating thumbnail: {e}")
            return ""
    
    async def generate_thumbnails(
        self,
        video_path: str,
        start_time: datetime,
        end_time: datetime,
        interval_seconds: int = 60
    ) -> List[str]:
        """Generate multiple thumbnails at intervals."""
        thumbnails = []
        current_time = start_time
        
        while current_time < end_time:
            output_path = os.path.join(
                self.output_dir,
                f"thumb_{current_time.strftime('%Y%m%d_%H%M%S')}.jpg"
            )
            
            thumbnail = await self.generate_thumbnail(video_path, current_time, output_path)
            if thumbnail:
                thumbnails.append(thumbnail)
            
            current_time += timedelta(seconds=interval_seconds)
        
        return thumbnails
