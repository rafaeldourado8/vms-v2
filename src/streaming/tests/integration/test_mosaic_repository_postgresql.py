"""Integration tests for MosaicRepositoryPostgreSQL."""
import pytest
import pytest_asyncio
from uuid import uuid4

from streaming.infrastructure.persistence.mosaic_repository_postgresql import MosaicRepositoryPostgreSQL
from streaming.domain.entities.mosaic import Mosaic
from shared_kernel.infrastructure.persistence.connection import get_postgres_connection_string


@pytest_asyncio.fixture
async def repository():
    repo = MosaicRepositoryPostgreSQL(get_postgres_connection_string())
    yield repo
    await repo.close()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_save_and_find_mosaic(repository):
    """Test saving and finding a mosaic."""
    user_id = uuid4()
    camera_ids = [uuid4(), uuid4()]
    
    mosaic = Mosaic(
        id=uuid4(),
        user_id=user_id,
        name="Test Mosaic",
        layout="2x2",
        camera_ids=camera_ids
    )
    
    await repository.save(mosaic)
    found = await repository.find_by_id(mosaic.id)
    
    assert found is not None
    assert found.id == mosaic.id
    assert found.user_id == user_id
    assert found.name == "Test Mosaic"
    assert found.layout == "2x2"
    assert len(found.camera_ids) == 2
    assert found.camera_ids == camera_ids
    
    await repository.delete(mosaic.id)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_find_by_user_id(repository):
    """Test finding mosaics by user ID."""
    user_id = uuid4()
    
    mosaic1 = Mosaic(id=uuid4(), user_id=user_id, name="Mosaic 1", camera_ids=[uuid4()])
    mosaic2 = Mosaic(id=uuid4(), user_id=user_id, name="Mosaic 2", camera_ids=[uuid4(), uuid4()])
    
    await repository.save(mosaic1)
    await repository.save(mosaic2)
    
    mosaics = await repository.find_by_user_id(user_id)
    
    assert len(mosaics) == 2
    assert any(m.name == "Mosaic 1" for m in mosaics)
    assert any(m.name == "Mosaic 2" for m in mosaics)
    
    await repository.delete(mosaic1.id)
    await repository.delete(mosaic2.id)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_update_mosaic(repository):
    """Test updating a mosaic."""
    mosaic = Mosaic(
        id=uuid4(),
        user_id=uuid4(),
        name="Original",
        layout="2x2",
        camera_ids=[uuid4()]
    )
    
    await repository.save(mosaic)
    
    mosaic.name = "Updated"
    mosaic.layout = "3x3"
    mosaic.add_camera(uuid4())
    
    await repository.save(mosaic)
    found = await repository.find_by_id(mosaic.id)
    
    assert found.name == "Updated"
    assert found.layout == "3x3"
    assert len(found.camera_ids) == 2
    
    await repository.delete(mosaic.id)
