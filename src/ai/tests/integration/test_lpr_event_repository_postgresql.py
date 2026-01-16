"""Integration tests for LPREventRepositoryPostgreSQL."""
import pytest
import pytest_asyncio
from uuid import uuid4
from datetime import datetime, timedelta

from ai.infrastructure.persistence.lpr_event_repository_postgresql import LPREventRepositoryPostgreSQL
from ai.domain.entities.lpr_event import LPREvent
from shared_kernel.infrastructure.persistence.connection import get_postgres_connection_string


@pytest_asyncio.fixture
async def repository():
    repo = LPREventRepositoryPostgreSQL(get_postgres_connection_string())
    yield repo
    await repo.close()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_save_and_find_lpr_event(repository):
    """Test saving and finding an LPR event."""
    camera_id = uuid4()
    
    event = LPREvent(
        id=uuid4(),
        camera_id=camera_id,
        plate="ABC1234",
        confidence=0.95,
        image_url="s3://bucket/image.jpg",
        detected_at=datetime.now(),
        city_id=None  # Sem city_id para evitar FK constraint
    )
    
    await repository.save(event)
    found = await repository.find_by_id(event.id)
    
    assert found is not None
    assert found.id == event.id
    assert found.camera_id == camera_id
    assert found.plate == "ABC1234"
    assert found.confidence == 0.95
    assert found.image_url == "s3://bucket/image.jpg"
    assert found.city_id is None
    
    await repository.delete(event.id)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_find_by_plate(repository):
    """Test finding events by plate."""
    camera_id = uuid4()
    
    event1 = LPREvent(id=uuid4(), camera_id=camera_id, plate="XYZ9999", confidence=0.9)
    event2 = LPREvent(id=uuid4(), camera_id=camera_id, plate="XYZ9999", confidence=0.85)
    
    await repository.save(event1)
    await repository.save(event2)
    
    events = await repository.find_by_plate("XYZ9999")
    
    assert len(events) >= 2
    assert all(e.plate == "XYZ9999" for e in events)
    
    await repository.delete(event1.id)
    await repository.delete(event2.id)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_search_by_camera(repository):
    """Test searching events by camera ID."""
    camera_id = uuid4()
    
    event = LPREvent(id=uuid4(), camera_id=camera_id, plate="TEST123", confidence=0.88)
    await repository.save(event)
    
    events = await repository.search(camera_id=camera_id)
    
    assert len(events) >= 1
    assert any(e.id == event.id for e in events)
    
    await repository.delete(event.id)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_search_by_date_range(repository):
    """Test searching events by date range."""
    camera_id = uuid4()
    now = datetime.now()
    
    event = LPREvent(
        id=uuid4(),
        camera_id=camera_id,
        plate="DATE123",
        confidence=0.92,
        detected_at=now
    )
    
    await repository.save(event)
    
    start = now - timedelta(hours=1)
    end = now + timedelta(hours=1)
    events = await repository.search(start_date=start, end_date=end)
    
    assert len(events) >= 1
    assert any(e.id == event.id for e in events)
    
    await repository.delete(event.id)
