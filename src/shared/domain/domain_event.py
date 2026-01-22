"""Domain Event base class for DDD."""
from abc import ABC
from datetime import datetime
from uuid import UUID, uuid4


class DomainEvent(ABC):
    """Base class for all domain events."""

    def __init__(self) -> None:
        """Initialize domain event."""
        self.event_id: UUID = uuid4()
        self.occurred_at: datetime = datetime.utcnow()

    def __repr__(self) -> str:
        """String representation of event."""
        return f"{self.__class__.__name__}(event_id={self.event_id}, occurred_at={self.occurred_at})"
