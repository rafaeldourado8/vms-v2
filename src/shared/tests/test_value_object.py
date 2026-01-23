"""Tests for ValueObject base class."""
import pytest

from src.shared.domain.value_object import ValueObject


class Money(ValueObject):
    """Test value object."""

    def __init__(self, amount: float, currency: str) -> None:
        self.amount = amount
        self.currency = currency


@pytest.mark.unit
def test_value_object_equality_by_value() -> None:
    """Test value objects are equal if values are equal."""
    money1 = Money(100.0, "USD")
    money2 = Money(100.0, "USD")
    assert money1 == money2


@pytest.mark.unit
def test_value_object_inequality_by_value() -> None:
    """Test value objects are not equal if values differ."""
    money1 = Money(100.0, "USD")
    money2 = Money(200.0, "USD")
    assert money1 != money2


@pytest.mark.unit
def test_value_object_hash() -> None:
    """Test value objects can be hashed."""
    money = Money(100.0, "USD")
    assert isinstance(hash(money), int)


@pytest.mark.unit
def test_value_object_same_hash_for_equal_values() -> None:
    """Test equal value objects have same hash."""
    money1 = Money(100.0, "USD")
    money2 = Money(100.0, "USD")
    assert hash(money1) == hash(money2)
