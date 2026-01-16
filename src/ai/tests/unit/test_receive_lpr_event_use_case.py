"""Tests for ReceiveLPREventUseCase."""
import pytest
from uuid import uuid4
from datetime import datetime
from src.ai.application.use_cases.receive_lpr_event import ReceiveLPREventUseCase
from src.ai.application.dtos.receive_lpr_event_dto import ReceiveLPREventDTO
from src.ai.infrastructure.persistence.lpr_event_repository_impl import LPREventRepositoryImpl
from src.streaming.infrastructure.external_services.storage_service_impl import MinIOStorageService


@pytest.mark.asyncio
async def test_receive_lpr_event_success():
    """Test receive LPR event success."""
    lpr_event_repository = LPREventRepositoryImpl()
    storage_service = MinIOStorageService()
    
    dto = ReceiveLPREventDTO(
        camera_id=uuid4(),
        plate="ABC1234",
        confidence=0.95,
        detected_at=datetime.utcnow()
    )
    use_case = ReceiveLPREventUseCase(lpr_event_repository, storage_service)
    
    result = await use_case.execute(dto)
    
    assert result.plate == "ABC1234"
    assert result.confidence == 0.95


@pytest.mark.asyncio
async def test_receive_lpr_event_with_city():
    """Test receive LPR event with city."""
    lpr_event_repository = LPREventRepositoryImpl()
    storage_service = MinIOStorageService()
    
    city_id = uuid4()
    dto = ReceiveLPREventDTO(
        camera_id=uuid4(),
        plate="XYZ5678",
        confidence=0.88,
        city_id=city_id
    )
    use_case = ReceiveLPREventUseCase(lpr_event_repository, storage_service)
    
    result = await use_case.execute(dto)
    
    assert result.city_id == city_id
