"""Tests for EventBus."""
import pytest

from src.shared.application.event_bus import EventBus
from src.shared.domain.domain_event import DomainEvent


class SampleEvent(DomainEvent):
    """Sample event for testing."""

    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message


@pytest.mark.unit
@pytest.mark.asyncio
async def test_event_bus_publishes_to_subscribers() -> None:
    """Test event bus publishes events to subscribers."""
    bus = EventBus()
    received_events = []

    async def handler(event: SampleEvent) -> None:
        received_events.append(event)

    bus.subscribe(SampleEvent, handler)
    event = SampleEvent("test message")
    await bus.publish(event)

    assert len(received_events) == 1
    assert received_events[0].message == "test message"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_event_bus_multiple_subscribers() -> None:
    """Test event bus publishes to multiple subscribers."""
    bus = EventBus()
    received_count = []

    async def handler1(event: SampleEvent) -> None:
        received_count.append(1)

    async def handler2(event: SampleEvent) -> None:
        received_count.append(2)

    bus.subscribe(SampleEvent, handler1)
    bus.subscribe(SampleEvent, handler2)
    await bus.publish(SampleEvent("test"))

    assert len(received_count) == 2
