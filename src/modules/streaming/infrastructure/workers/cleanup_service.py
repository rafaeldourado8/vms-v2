"""Cleanup service for expired recordings."""
import asyncio
from src.streaming.infrastructure.persistence.recording_repository_impl import RecordingRepositoryImpl
from src.streaming.infrastructure.external_services.storage_service_impl import MinIOStorageService
from src.shared.infrastructure.logger import Logger


class CleanupService:
    """Cleanup service for expired recordings."""
    
    def __init__(self):
        self.logger = Logger(__name__)
        self.recording_repository = RecordingRepositoryImpl()
        self.storage_service = MinIOStorageService()
    
    async def run(self):
        """Run cleanup process."""
        try:
            expired_recordings = await self.recording_repository.find_expired()
            
            for recording in expired_recordings:
                try:
                    if recording.storage_path:
                        await self.storage_service.delete_file(recording.storage_path)
                    
                    await self.recording_repository.delete(recording.id)
                    self.logger.info(f"Deleted expired recording {recording.id}")
                    
                except Exception as e:
                    self.logger.error(f"Failed to delete recording {recording.id}: {e}")
            
            self.logger.info(f"Cleanup completed. Deleted {len(expired_recordings)} recordings")
            
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")


async def main():
    """Main cleanup entry point."""
    service = CleanupService()
    while True:
        await service.run()
        await asyncio.sleep(3600)  # Run every hour


if __name__ == "__main__":
    asyncio.run(main())
