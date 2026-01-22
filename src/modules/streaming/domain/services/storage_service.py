"""Storage service interface."""
from abc import ABC, abstractmethod
from typing import Optional


class StorageService(ABC):
    """Storage service interface."""
    
    @abstractmethod
    async def upload_file(self, local_path: str, remote_path: str) -> str:
        """Upload file to storage."""
        pass
    
    @abstractmethod
    async def delete_file(self, remote_path: str) -> bool:
        """Delete file from storage."""
        pass
    
    @abstractmethod
    async def get_file_url(self, remote_path: str, expires_in: int = 3600) -> Optional[str]:
        """Get presigned URL for file."""
        pass
    
    @abstractmethod
    async def file_exists(self, remote_path: str) -> bool:
        """Check if file exists."""
        pass
