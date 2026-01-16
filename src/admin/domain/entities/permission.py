"""Permission entity."""
from uuid import UUID

from src.shared_kernel.domain.entity import Entity


class Permission(Entity):
    """Permission entity."""

    def __init__(
        self,
        entity_id: UUID | None = None,
        name: str = "",
        code: str = "",
        description: str = "",
    ) -> None:
        """Initialize permission."""
        super().__init__(entity_id)
        self.name = name
        self.code = code
        self.description = description

    def __repr__(self) -> str:
        """String representation."""
        return f"Permission(id={self.id}, code={self.code})"
