"""Role repository interface."""
from abc import abstractmethod
from typing import Optional

from src.admin.domain.entities.role import Role
from src.shared_kernel.domain.repository import Repository


class IRoleRepository(Repository[Role]):
    """Role repository interface."""

    @abstractmethod
    async def find_by_code(self, code: str) -> Optional[Role]:
        """Find role by code."""
        pass
