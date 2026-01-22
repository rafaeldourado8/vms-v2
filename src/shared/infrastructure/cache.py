"""Cache configuration and utilities."""
from typing import Any, Optional

import redis.asyncio as aioredis


class CacheConfig:
    """Redis cache configuration."""

    def __init__(self, redis_url: str) -> None:
        """Initialize cache config."""
        self.redis = aioredis.from_url(redis_url, decode_responses=True)

    async def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        return await self.redis.get(key)

    async def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set value in cache with TTL."""
        await self.redis.setex(key, ttl, value)

    async def delete(self, key: str) -> None:
        """Delete key from cache."""
        await self.redis.delete(key)

    async def close(self) -> None:
        """Close cache connection."""
        await self.redis.close()
