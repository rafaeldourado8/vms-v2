"""Role repository implementation."""
from typing import List, Optional
from uuid import UUID

from src.admin.domain.entities.permission import Permission
from src.admin.domain.entities.role import Role
from src.admin.domain.repositories.role_repository import IRoleRepository
from src.admin.infrastructure.persistence.models import RoleModel


class RoleRepository(IRoleRepository):
    """Role repository implementation using Django ORM."""

    async def save(self, aggregate: Role) -> None:
        """Save role."""
        role_model, created = await RoleModel.objects.aget_or_create(
            id=aggregate.id,
            defaults={"name": aggregate.name, "code": aggregate.code},
        )

        if not created:
            role_model.name = aggregate.name
            role_model.code = aggregate.code
            await role_model.asave()

        await role_model.permissions.aset([p.id for p in aggregate.permissions])

    async def find_by_id(self, aggregate_id: UUID) -> Optional[Role]:
        """Find role by ID."""
        try:
            role_model = await RoleModel.objects.prefetch_related("permissions").aget(
                id=aggregate_id
            )
            return self._to_domain(role_model)
        except RoleModel.DoesNotExist:
            return None

    async def find_by_code(self, code: str) -> Optional[Role]:
        """Find role by code."""
        try:
            role_model = await RoleModel.objects.prefetch_related("permissions").aget(
                code=code
            )
            return self._to_domain(role_model)
        except RoleModel.DoesNotExist:
            return None

    async def find_all(self) -> List[Role]:
        """Find all roles."""
        role_models = RoleModel.objects.prefetch_related("permissions").all()
        return [self._to_domain(rm) async for rm in role_models]

    async def delete(self, aggregate_id: UUID) -> None:
        """Delete role."""
        await RoleModel.objects.filter(id=aggregate_id).adelete()

    def _to_domain(self, role_model: RoleModel) -> Role:
        """Convert Django model to domain entity."""
        permissions = [
            Permission(
                entity_id=p.id,
                name=p.name,
                code=p.code,
                description=p.description,
            )
            for p in role_model.permissions.all()
        ]

        return Role(
            entity_id=role_model.id,
            name=role_model.name,
            code=role_model.code,
            permissions=permissions,
        )
