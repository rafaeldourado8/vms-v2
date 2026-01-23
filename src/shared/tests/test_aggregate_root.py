"""Tests for AggregateRoot base class."""
import pytest

from src.shared.domain.aggregate_root import AggregateRoot
from src.shared.domain.domain_event import DomainEvent


class SampleEvent(DomainEvent):
    """Sample event for testing."""

    def __init__(self, data: str) -> None:
        super().__init__()
        self.data = data


class SampleAggregate(AggregateRoot):
    """Sample aggregate for testing."""

    def do_something(self) -> None:
        """Do something and raise event."""
        self.add_domain_event(SampleEvent("something happened"))


@pytest.mark.unit
def test_aggregate_collects_domain_events() -> None:
    """Test aggregate collects domain events."""
    aggregate = SampleAggregate()
    aggregate.do_something()
    events = aggregate.domain_events
    assert len(events) == 1
    assert isinstance(events[0], SampleEvent)


@pytest.mark.unit
def test_aggregate_clears_domain_events() -> None:
    """Test aggregate can clear domain events."""
    aggregate = SampleAggregate()
    aggregate.do_something()
    aggregate.clear_domain_events()
    assert len(aggregate.domain_events) == 0


@pytest.mark.unit
def test_aggregate_returns_copy_of_events() -> None:
    """Test aggregate returns copy of events list."""
    aggregate = SampleAggregate()
    aggregate.do_something()
    events1 = aggregate.domain_events
    events2 = aggregate.domain_events
    assert events1 is not events2
    assert events1 == events2
