"""PostgreSQL repository base class."""
from typing import Optional, TypeVar, Generic
from uuid import UUID
import asyncpg
from contextlib import asynccontextmanager

from shared_kernel.domain.repository import Repository

T = TypeVar('T')


class PostgreSQLRepository(Repository[T], Generic[T]):
    """Base class for PostgreSQL repositories."""
    
    def __init__(self, connection_string: str):
        """Initialize repository.
        
        Args:
            connection_string: postgresql://user:pass@host:port/dbname
        """
        self.connection_string = connection_string
        self._pool: Optional[asyncpg.Pool] = None
    
    async def _get_pool(self) -> asyncpg.Pool:
        """Get or create connection pool."""
        if self._pool is None:
            self._pool = await asyncpg.create_pool(
                self.connection_string,
                min_size=2,
                max_size=10,
                command_timeout=60
            )
        return self._pool
    
    @asynccontextmanager
    async def _connection(self):
        """Get database connection."""
        pool = await self._get_pool()
        async with pool.acquire() as conn:
            yield conn
    
    @asynccontextmanager
    async def _transaction(self):
        """Get database transaction."""
        async with self._connection() as conn:
            async with conn.transaction():
                yield conn
    
    async def close(self):
        """Close connection pool."""
        if self._pool:
            await self._pool.close()
            self._pool = None
