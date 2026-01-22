"""FFmpeg service implementation."""
import asyncio
import os
from uuid import UUID
from typing import Dict
from src.streaming.domain.services.ffmpeg_service import FFmpegService
from src.shared_kernel.infrastructure.logger import Logger


class FFmpegServiceImpl(FFmpegService):
    """FFmpeg service implementation."""
    
    def __init__(self):
        self.logger = Logger(__name__)
        self.processes: Dict[UUID, asyncio.subprocess.Process] = {}
    
    async def start_recording(self, recording_id: UUID, source_url: str, output_path: str) -> bool:
        """Start recording from RTSP source."""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            cmd = [
                "ffmpeg",
                "-i", source_url,
                "-c:v", "copy",
                "-c:a", "copy",
                "-f", "segment",
                "-segment_time", "3600",
                "-strftime", "1",
                "-reset_timestamps", "1",
                f"{output_path}_%Y%m%d_%H%M%S.mp4"
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            self.processes[recording_id] = process
            self.logger.info(f"Started recording {recording_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start recording: {e}")
            return False
    
    async def stop_recording(self, recording_id: UUID) -> bool:
        """Stop recording."""
        try:
            process = self.processes.get(recording_id)
            if not process:
                return False
            
            process.terminate()
            await process.wait()
            del self.processes[recording_id]
            
            self.logger.info(f"Stopped recording {recording_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop recording: {e}")
            return False
    
    async def is_recording(self, recording_id: UUID) -> bool:
        """Check if recording is active."""
        process = self.processes.get(recording_id)
        return process is not None and process.returncode is None
