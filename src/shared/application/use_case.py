"""Use Case base class for application layer."""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class UseCase(ABC, Generic[InputDTO, OutputDTO]):
    """Base class for use cases."""

    @abstractmethod
    async def execute(self, input_dto: InputDTO) -> OutputDTO:
        """Execute use case."""
        pass
