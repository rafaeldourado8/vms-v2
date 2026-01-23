"""Clip service implementation using FFmpeg."""
import os
import asyncio
from datetime import datetime
from src.streaming.domain.services.clip_service import ClipService
from src.shared.infrastructure.logger import Logger


class ClipServiceImpl(ClipService):
    """Clip service implementation."""
    
    def __init__(self):
        self.logger = Logger(__name__)
    
    async def create_clip(
        self,
        source_path: str,
        output_path: str,
        start_time: datetime,
        end_time: datetime
    ) -> bool:
        """Create clip from video."""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            duration = int((end_time - start_time).total_seconds())
            
            cmd = [
                "ffmpeg",
                "-i", source_path,
                "-ss", start_time.strftime("%H:%M:%S"),
                "-t", str(duration),
                "-c:v", "copy",
                "-c:a", "copy",
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
                self.logger.info(f"Clip created: {output_path}")
                return True
            else:
                self.logger.error(f"Failed to create clip: {process.returncode}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error creating clip: {e}")
            return False
