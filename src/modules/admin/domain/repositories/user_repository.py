"""User repository interface."""
from abc import abstractmethod
from typing import Optional

from src.modules.admin.domain.aggregates.user import User
from src.modules.admin.domain.value_objects.email import Email
from src.shared.domain.repository import Repository


class IUserRepository(Repository[User]):
    """User repository interface."""

    @abstractmethod
    async def find_by_email(self, email: Email) -> Optional[User]:
        """Find user by email."""
        pass

    @abstractmethod
    async def email_exists(self, email: Email) -> bool:
        """Check if email already exists."""
        pass
