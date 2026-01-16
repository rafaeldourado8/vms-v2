"""Integration tests for MinIOStorageService."""
import pytest
import pytest_asyncio
import os
import tempfile
from uuid import uuid4

from streaming.infrastructure.external_services.storage_service_impl import MinIOStorageService


@pytest_asyncio.fixture
async def storage_service():
    service = MinIOStorageService()
    yield service


@pytest.mark.asyncio
@pytest.mark.integration
async def test_upload_and_file_exists(storage_service):
    """Test uploading a file and checking if it exists."""
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Test content for MinIO")
        temp_file = f.name
    
    try:
        remote_path = f"test/{uuid4()}.txt"
        
        # Upload file
        result = await storage_service.upload_file(temp_file, remote_path)
        
        assert result.startswith("s3://")
        assert remote_path in result
        
        # Check if file exists
        exists = await storage_service.file_exists(remote_path)
        assert exists is True
        
        # Cleanup
        await storage_service.delete_file(remote_path)
    finally:
        os.unlink(temp_file)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_presigned_url(storage_service):
    """Test getting presigned URL for a file."""
    # Create and upload temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Test content for presigned URL")
        temp_file = f.name
    
    try:
        remote_path = f"test/{uuid4()}.txt"
        
        await storage_service.upload_file(temp_file, remote_path)
        
        # Get presigned URL
        url = await storage_service.get_file_url(remote_path, expires_in=300)
        
        assert url is not None
        assert "http" in url
        assert remote_path in url
        
        # Cleanup
        await storage_service.delete_file(remote_path)
    finally:
        os.unlink(temp_file)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_delete_file(storage_service):
    """Test deleting a file."""
    # Create and upload temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Test content for deletion")
        temp_file = f.name
    
    try:
        remote_path = f"test/{uuid4()}.txt"
        
        await storage_service.upload_file(temp_file, remote_path)
        
        # Verify file exists
        exists_before = await storage_service.file_exists(remote_path)
        assert exists_before is True
        
        # Delete file
        deleted = await storage_service.delete_file(remote_path)
        assert deleted is True
        
        # Verify file no longer exists
        exists_after = await storage_service.file_exists(remote_path)
        assert exists_after is False
    finally:
        os.unlink(temp_file)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_file_not_exists(storage_service):
    """Test checking for non-existent file."""
    remote_path = f"test/nonexistent_{uuid4()}.txt"
    
    exists = await storage_service.file_exists(remote_path)
    assert exists is False


@pytest.mark.asyncio
@pytest.mark.integration
async def test_upload_multiple_files(storage_service):
    """Test uploading multiple files."""
    files_to_cleanup = []
    temp_files = []
    
    try:
        # Create and upload 3 files
        for i in range(3):
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
                f.write(f"Test content {i}")
                temp_files.append(f.name)
            
            remote_path = f"test/multi_{uuid4()}.txt"
            files_to_cleanup.append(remote_path)
            
            result = await storage_service.upload_file(temp_files[i], remote_path)
            assert result.startswith("s3://")
        
        # Verify all files exist
        for remote_path in files_to_cleanup:
            exists = await storage_service.file_exists(remote_path)
            assert exists is True
        
        # Cleanup
        for remote_path in files_to_cleanup:
            await storage_service.delete_file(remote_path)
    finally:
        for temp_file in temp_files:
            os.unlink(temp_file)
