"""UserAuthenticated domain event."""
from uuid import UUID

from src.shared_kernel.domain.domain_event import DomainEvent


class UserAuthenticated(DomainEvent):
    """Event raised when user authenticates."""

    def __init__(self, user_id: UUID, email: str) -> None:
        """Initialize event."""
        super().__init__()
        self.user_id = user_id
        self.email = email
