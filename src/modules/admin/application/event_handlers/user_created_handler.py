"""User Created Event Handler."""
from src.modules.admin.domain.events.user_created import UserCreated
from src.shared.infrastructure.logger import setup_logger

logger = setup_logger(__name__)


class UserCreatedEventHandler:
    """Handler for UserCreated event."""

    async def handle(self, event: UserCreated) -> None:
        """Handle UserCreated event."""
        logger.info(
            f"User created: {event.user_id}",
            extra={"user_id": str(event.user_id), "email": event.email, "name": event.name},
        )
