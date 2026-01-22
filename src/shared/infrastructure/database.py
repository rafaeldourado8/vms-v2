"""Database configuration and utilities."""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class DatabaseConfig:
    """Database configuration."""

    def __init__(self, database_url: str) -> None:
        """Initialize database config."""
        self.engine = create_async_engine(database_url, echo=False, pool_pre_ping=True)
        self.async_session_factory = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session."""
        async with self.async_session_factory() as session:
            yield session

    async def close(self) -> None:
        """Close database connection."""
        await self.engine.dispose()
