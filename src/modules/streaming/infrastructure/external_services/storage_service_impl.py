"""Storage service implementation using MinIO/S3."""
import os
from typing import Optional
from minio import Minio
from minio.error import S3Error
from src.streaming.domain.services.storage_service import StorageService
from src.shared.infrastructure.logger import Logger


class MinIOStorageService(StorageService):
    """MinIO storage service implementation."""
    
    def __init__(self):
        self.logger = Logger(__name__)
        endpoint = os.getenv("MINIO_ENDPOINT", os.getenv("STORAGE_ENDPOINT", "localhost:9000"))
        self.client = Minio(
            endpoint.replace("http://", "").replace("https://", ""),
            access_key=os.getenv("MINIO_ACCESS_KEY", os.getenv("STORAGE_ACCESS_KEY", "minioadmin")),
            secret_key=os.getenv("MINIO_SECRET_KEY", os.getenv("STORAGE_SECRET_KEY", "minioadmin")),
            secure=False
        )
        self.bucket = os.getenv("STORAGE_BUCKET_RECORDINGS", "recordings")
        try:
            self._ensure_bucket()
        except Exception as e:
            self.logger.warning(f"Could not ensure bucket on init: {e}")
    
    def _ensure_bucket(self):
        """Ensure bucket exists."""
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
        except S3Error as e:
            self.logger.error(f"Failed to create bucket: {e}")
    
    async def upload_file(self, local_path: str, remote_path: str) -> str:
        """Upload file to storage."""
        try:
            self.client.fput_object(self.bucket, remote_path, local_path)
            return f"s3://{self.bucket}/{remote_path}"
        except S3Error as e:
            self.logger.error(f"Failed to upload file: {e}")
            raise
    
    async def delete_file(self, remote_path: str) -> bool:
        """Delete file from storage."""
        try:
            self.client.remove_object(self.bucket, remote_path)
            return True
        except S3Error as e:
            self.logger.error(f"Failed to delete file: {e}")
            return False
    
    async def get_file_url(self, remote_path: str, expires_in: int = 3600) -> Optional[str]:
        """Get presigned URL for file."""
        try:
            from datetime import timedelta
            url = self.client.presigned_get_object(
                self.bucket,
                remote_path,
                expires=timedelta(seconds=expires_in)
            )
            return url
        except S3Error as e:
            self.logger.error(f"Failed to get file URL: {e}")
            return None
    
    async def file_exists(self, remote_path: str) -> bool:
        """Check if file exists."""
        try:
            self.client.stat_object(self.bucket, remote_path)
            return True
        except S3Error:
            return False
