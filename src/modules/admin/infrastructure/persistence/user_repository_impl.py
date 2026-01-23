"""User repository implementation."""
from typing import List, Optional
from uuid import UUID

from src.modules.admin.domain.aggregates.user import User
from src.modules.admin.domain.entities.permission import Permission
from src.modules.admin.domain.entities.role import Role
from src.modules.admin.domain.repositories.user_repository import IUserRepository
from src.modules.admin.domain.value_objects.email import Email
from src.modules.admin.domain.value_objects.password import Password
from src.modules.admin.infrastructure.persistence.models import UserModel


class UserRepository(IUserRepository):
    """User repository implementation using Django ORM."""

    async def save(self, aggregate: User) -> None:
        """Save user aggregate."""
        user_model, created = await UserModel.objects.aget_or_create(
            id=aggregate.id,
            defaults={
                "email": aggregate.email.value,
                "name": aggregate.name,
                "is_active": aggregate.is_active,
                "login_attempts": aggregate.login_attempts,
            },
        )

        if not created:
            user_model.email = aggregate.email.value
            user_model.name = aggregate.name
            user_model.is_active = aggregate.is_active
            user_model.login_attempts = aggregate.login_attempts
            await user_model.asave()

        user_model.password = aggregate.password.value
        await user_model.asave()

        await user_model.roles.aset([role.id for role in aggregate.roles])

    async def find_by_id(self, aggregate_id: UUID) -> Optional[User]:
        """Find user by ID."""
        try:
            user_model = await UserModel.objects.prefetch_related(
                "roles__permissions"
            ).aget(id=aggregate_id)
            return self._to_domain(user_model)
        except UserModel.DoesNotExist:
            return None

    async def find_by_email(self, email: Email) -> Optional[User]:
        """Find user by email."""
        try:
            user_model = await UserModel.objects.prefetch_related(
                "roles__permissions"
            ).aget(email=email.value)
            return self._to_domain(user_model)
        except UserModel.DoesNotExist:
            return None

    async def email_exists(self, email: Email) -> bool:
        """Check if email exists."""
        return await UserModel.objects.filter(email=email.value).aexists()

    async def find_all(self) -> List[User]:
        """Find all users."""
        user_models = UserModel.objects.prefetch_related("roles__permissions").all()
        return [self._to_domain(um) async for um in user_models]

    async def delete(self, aggregate_id: UUID) -> None:
        """Delete user."""
        await UserModel.objects.filter(id=aggregate_id).adelete()

    def _to_domain(self, user_model: UserModel) -> User:
        """Convert Django model to domain aggregate."""
        roles = []
        for role_model in user_model.roles.all():
            permissions = [
                Permission(
                    entity_id=p.id,
                    name=p.name,
                    code=p.code,
                    description=p.description,
                )
                for p in role_model.permissions.all()
            ]
            roles.append(
                Role(
                    entity_id=role_model.id,
                    name=role_model.name,
                    code=role_model.code,
                    permissions=permissions,
                )
            )

        return User(
            entity_id=user_model.id,
            email=Email(user_model.email),
            password=Password(user_model.password, hashed=True),
            name=user_model.name,
            is_active=user_model.is_active,
            roles=roles,
        )
