"""Event Bus for domain events."""
from typing import Callable, Dict, List, Type

from src.shared.domain.domain_event import DomainEvent


class EventBus:
    """Simple in-memory event bus."""

    def __init__(self) -> None:
        """Initialize event bus."""
        self._handlers: Dict[Type[DomainEvent], List[Callable]] = {}

    def subscribe(self, event_type: Type[DomainEvent], handler: Callable) -> None:
        """Subscribe handler to event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def publish(self, event: DomainEvent) -> None:
        """Publish event to all subscribers."""
        event_type = type(event)
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                await handler(event)
