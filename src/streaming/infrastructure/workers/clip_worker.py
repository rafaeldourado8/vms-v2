"""RabbitMQ worker for clip processing."""
import asyncio
from uuid import UUID
from datetime import datetime

from shared_kernel.infrastructure.message_broker import MessageBrokerConfig
from shared_kernel.infrastructure.rabbitmq_connection import get_rabbitmq_url
from shared_kernel.infrastructure.persistence.connection import get_postgres_connection_string
from streaming.infrastructure.external_services.clip_service_impl import ClipServiceImpl
from streaming.infrastructure.persistence.clip_repository_postgresql import ClipRepositoryPostgreSQL
from shared_kernel.infrastructure.logger import Logger


class ClipWorker:
    """Clip worker with PostgreSQL and RabbitMQ."""
    
    def __init__(self):
        self.logger = Logger(__name__)
        self.message_broker = MessageBrokerConfig(get_rabbitmq_url(), max_retries=3)
        self.clip_service = ClipServiceImpl()
        self.clip_repository = ClipRepositoryPostgreSQL(get_postgres_connection_string())
    
    async def start(self):
        """Start worker."""
        self.logger.info("Starting ClipWorker...")
        await self.message_broker.connect()
        await self.message_broker.consume(
            queue="clips",
            callback=self.process_message
        )
        self.logger.info("ClipWorker started and listening for messages")
    
    async def process_message(self, message: dict):
        """Process clip message."""
        try:
            clip_id = UUID(message["clip_id"])
            source_path = message["source_path"]
            start_time = datetime.fromisoformat(message["start_time"])
            end_time = datetime.fromisoformat(message["end_time"])
            
            self.logger.info(f"Processing clip {clip_id}")
            
            clip = await self.clip_repository.find_by_id(clip_id)
            if not clip:
                self.logger.error(f"Clip {clip_id} not found")
                return
            
            clip.mark_processing()
            await self.clip_repository.save(clip)
            
            output_path = f"/clips/{clip.recording_id}/{clip_id}.mp4"
            
            success = await self.clip_service.create_clip(
                source_path,
                output_path,
                start_time,
                end_time
            )
            
            if success:
                import os
                file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
                clip.mark_completed(output_path, file_size_mb)
                await self.clip_repository.save(clip)
                self.logger.info(f"Clip {clip_id} completed successfully")
            else:
                clip.mark_error()
                await self.clip_repository.save(clip)
                self.logger.error(f"Failed to create clip {clip_id}")
                
        except Exception as e:
            self.logger.error(f"Error processing clip message: {e}")
            raise
    
    async def stop(self):
        """Stop worker and cleanup."""
        self.logger.info("Stopping ClipWorker...")
        await self.clip_repository.close()
        await self.message_broker.close()
        self.logger.info("ClipWorker stopped")


async def main():
    """Main worker entry point."""
    worker = ClipWorker()
    try:
        await worker.start()
        # Keep worker running
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        await worker.stop()


if __name__ == "__main__":
    asyncio.run(main())
