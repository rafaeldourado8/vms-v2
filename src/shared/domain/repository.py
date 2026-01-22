"""Repository interface for DDD."""
from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from src.shared_kernel.domain.aggregate_root import AggregateRoot

T = TypeVar("T", bound=AggregateRoot)


class Repository(ABC, Generic[T]):
    """Base repository interface."""

    @abstractmethod
    async def save(self, aggregate: T) -> None:
        """Save aggregate."""
        pass

    @abstractmethod
    async def find_by_id(self, aggregate_id: UUID) -> Optional[T]:
        """Find aggregate by ID."""
        pass

    @abstractmethod
    async def find_all(self) -> List[T]:
        """Find all aggregates."""
        pass

    @abstractmethod
    async def delete(self, aggregate_id: UUID) -> None:
        """Delete aggregate."""
        pass
