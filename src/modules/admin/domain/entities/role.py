"""Role entity."""
from typing import List
from uuid import UUID

from src.modules.admin.domain.entities.permission import Permission
from src.shared.domain.entity import Entity


class Role(Entity):
    """Role entity with permissions."""

    def __init__(
        self,
        entity_id: UUID | None = None,
        name: str = "",
        code: str = "",
        permissions: List[Permission] | None = None,
    ) -> None:
        """Initialize role."""
        super().__init__(entity_id)
        self.name = name
        self.code = code
        self.permissions = permissions or []

    def add_permission(self, permission: Permission) -> None:
        """Add permission to role."""
        if permission not in self.permissions:
            self.permissions.append(permission)
            self._touch()

    def remove_permission(self, permission: Permission) -> None:
        """Remove permission from role."""
        if permission in self.permissions:
            self.permissions.remove(permission)
            self._touch()

    def has_permission(self, permission_code: str) -> bool:
        """Check if role has permission."""
        return any(p.code == permission_code for p in self.permissions)

    def __repr__(self) -> str:
        """String representation."""
        return f"Role(id={self.id}, code={self.code}, permissions={len(self.permissions)})"
