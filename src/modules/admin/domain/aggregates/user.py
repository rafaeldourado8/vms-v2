"""User aggregate root."""
from typing import List
from uuid import UUID

from src.admin.domain.entities.role import Role
from src.admin.domain.events.user_authenticated import UserAuthenticated
from src.admin.domain.events.user_created import UserCreated
from src.admin.domain.value_objects.email import Email
from src.admin.domain.value_objects.password import Password
from src.shared_kernel.domain.aggregate_root import AggregateRoot
from src.shared_kernel.domain.domain_exception import (
    BusinessRuleViolationException,
    ValidationException,
)


class User(AggregateRoot):
    """User aggregate root."""

    MAX_LOGIN_ATTEMPTS = 5

    def __init__(
        self,
        entity_id: UUID | None = None,
        email: Email | None = None,
        password: Password | None = None,
        name: str = "",
        is_active: bool = True,
        roles: List[Role] | None = None,
    ) -> None:
        """Initialize user."""
        super().__init__(entity_id)
        if email is None:
            raise ValidationException("Email is required")
        if password is None:
            raise ValidationException("Password is required")

        self.email = email
        self.password = password
        self.name = name
        self.is_active = is_active
        self.roles = roles or []
        self.login_attempts = 0

    @staticmethod
    def create(email: Email, password: Password, name: str) -> "User":
        """Factory method to create user."""
        user = User(email=email, password=password, name=name)
        user.add_domain_event(UserCreated(user.id, email.value, name))
        return user

    def authenticate(self, plain_password: str) -> None:
        """Authenticate user with password."""
        if not self.is_active:
            raise BusinessRuleViolationException("User is inactive")

        if self.login_attempts >= self.MAX_LOGIN_ATTEMPTS:
            raise BusinessRuleViolationException("Too many login attempts")

        if not self.password.verify(plain_password):
            self.login_attempts += 1
            self._touch()
            raise BusinessRuleViolationException("Invalid credentials")

        self.login_attempts = 0
        self._touch()
        self.add_domain_event(UserAuthenticated(self.id, self.email.value))

    def add_role(self, role: Role) -> None:
        """Add role to user."""
        if role not in self.roles:
            self.roles.append(role)
            self._touch()

    def remove_role(self, role: Role) -> None:
        """Remove role from user."""
        if role in self.roles:
            self.roles.remove(role)
            self._touch()

    def has_permission(self, permission_code: str) -> bool:
        """Check if user has permission."""
        return any(role.has_permission(permission_code) for role in self.roles)

    def deactivate(self) -> None:
        """Deactivate user."""
        self.is_active = False
        self._touch()

    def activate(self) -> None:
        """Activate user."""
        self.is_active = True
        self.login_attempts = 0
        self._touch()

    def __repr__(self) -> str:
        """String representation."""
        return f"User(id={self.id}, email={self.email}, active={self.is_active})"
