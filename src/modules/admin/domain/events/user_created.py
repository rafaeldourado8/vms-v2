"""UserCreated domain event."""
from uuid import UUID

from src.shared.domain.domain_event import DomainEvent


class UserCreated(DomainEvent):
    """Event raised when user is created."""

    def __init__(self, user_id: UUID, email: str, name: str) -> None:
        """Initialize event."""
        super().__init__()
        self.user_id = user_id
        self.email = email
        self.name = name
