"""RabbitMQ worker for recording processing."""
import asyncio
from uuid import UUID

from shared_kernel.infrastructure.message_broker import MessageBrokerConfig
from shared_kernel.infrastructure.rabbitmq_connection import get_rabbitmq_url
from shared_kernel.infrastructure.persistence.connection import get_postgres_connection_string
from streaming.infrastructure.external_services.ffmpeg_service_impl import FFmpegServiceImpl
from streaming.infrastructure.persistence.recording_repository_postgresql import RecordingRepositoryPostgreSQL
from shared_kernel.infrastructure.logger import Logger


class RecordingWorker:
    """Recording worker with PostgreSQL and RabbitMQ."""
    
    def __init__(self):
        self.logger = Logger(__name__)
        self.message_broker = MessageBrokerConfig(get_rabbitmq_url(), max_retries=3)
        self.ffmpeg_service = FFmpegServiceImpl()
        self.recording_repository = RecordingRepositoryPostgreSQL(get_postgres_connection_string())
    
    async def start(self):
        """Start worker."""
        self.logger.info("Starting RecordingWorker...")
        await self.message_broker.connect()
        await self.message_broker.consume(
            queue="recordings",
            callback=self.process_message
        )
        self.logger.info("RecordingWorker started and listening for messages")
    
    async def process_message(self, message: dict):
        """Process recording message."""
        try:
            recording_id = UUID(message["recording_id"])
            source_url = message["source_url"]
            
            self.logger.info(f"Processing recording {recording_id}")
            
            recording = await self.recording_repository.find_by_id(recording_id)
            if not recording:
                self.logger.error(f"Recording {recording_id} not found")
                return
            
            output_path = f"/recordings/{recording.stream_id}/{recording_id}"
            
            success = await self.ffmpeg_service.start_recording(
                recording_id,
                source_url,
                output_path
            )
            
            if success:
                recording.storage_path = output_path
                await self.recording_repository.save(recording)
                self.logger.info(f"Recording {recording_id} started successfully")
            else:
                recording.mark_error()
                await self.recording_repository.save(recording)
                self.logger.error(f"Failed to start recording {recording_id}")
                
        except Exception as e:
            self.logger.error(f"Error processing recording message: {e}")
            raise
    
    async def stop(self):
        """Stop worker and cleanup."""
        self.logger.info("Stopping RecordingWorker...")
        await self.recording_repository.close()
        await self.message_broker.close()
        self.logger.info("RecordingWorker stopped")


async def main():
    """Main worker entry point."""
    worker = RecordingWorker()
    try:
        await worker.start()
        # Keep worker running
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        await worker.stop()


if __name__ == "__main__":
    asyncio.run(main())
