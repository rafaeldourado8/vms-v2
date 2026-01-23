"""Tests for Entity base class."""
import pytest
from uuid import UUID

from src.shared.domain.entity import Entity


class SampleEntity(Entity):
    """Sample entity for testing."""

    def __init__(self, entity_id: UUID | None = None, name: str = "") -> None:
        super().__init__(entity_id)
        self.name = name


@pytest.mark.unit
def test_entity_creates_with_id() -> None:
    """Test entity is created with unique ID."""
    entity = SampleEntity()
    assert isinstance(entity.id, UUID)


@pytest.mark.unit
def test_entity_creates_with_custom_id() -> None:
    """Test entity can be created with custom ID."""
    from uuid import uuid4

    custom_id = uuid4()
    entity = SampleEntity(entity_id=custom_id)
    assert entity.id == custom_id


@pytest.mark.unit
def test_entity_has_timestamps() -> None:
    """Test entity has creation and update timestamps."""
    entity = SampleEntity()
    assert entity.created_at is not None
    assert entity.updated_at is not None


@pytest.mark.unit
def test_entity_equality_by_id() -> None:
    """Test entities are equal if they have same ID."""
    from uuid import uuid4

    entity_id = uuid4()
    entity1 = SampleEntity(entity_id=entity_id, name="Entity 1")
    entity2 = SampleEntity(entity_id=entity_id, name="Entity 2")
    assert entity1 == entity2


@pytest.mark.unit
def test_entity_inequality_by_id() -> None:
    """Test entities are not equal if they have different IDs."""
    entity1 = SampleEntity(name="Entity 1")
    entity2 = SampleEntity(name="Entity 2")
    assert entity1 != entity2


@pytest.mark.unit
def test_entity_hash() -> None:
    """Test entity can be hashed."""
    entity = SampleEntity()
    assert isinstance(hash(entity), int)
