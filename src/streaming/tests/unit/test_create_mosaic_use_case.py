"""Tests for CreateMosaicUseCase."""
import pytest
from uuid import uuid4
from src.streaming.application.use_cases.create_mosaic import CreateMosaicUseCase
from src.streaming.application.dtos.create_mosaic_dto import CreateMosaicDTO
from src.streaming.infrastructure.persistence.mosaic_repository_impl import MosaicRepositoryImpl


@pytest.mark.asyncio
async def test_create_mosaic_success():
    """Test create mosaic success."""
    mosaic_repository = MosaicRepositoryImpl()
    
    dto = CreateMosaicDTO(
        user_id=uuid4(),
        name="My Mosaic",
        layout="2x2",
        camera_ids=[uuid4(), uuid4()]
    )
    use_case = CreateMosaicUseCase(mosaic_repository)
    
    result = await use_case.execute(dto)
    
    assert result.name == "My Mosaic"
    assert result.layout == "2x2"
    assert len(result.camera_ids) == 2


@pytest.mark.asyncio
async def test_create_mosaic_empty():
    """Test create mosaic without cameras."""
    mosaic_repository = MosaicRepositoryImpl()
    
    dto = CreateMosaicDTO(
        user_id=uuid4(),
        name="Empty Mosaic"
    )
    use_case = CreateMosaicUseCase(mosaic_repository)
    
    result = await use_case.execute(dto)
    
    assert result.name == "Empty Mosaic"
    assert len(result.camera_ids) == 0
