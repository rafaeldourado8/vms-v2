"""Stream repository PostgreSQL implementation."""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from streaming.domain.entities.stream import Stream
from streaming.domain.value_objects.stream_status import StreamStatus
from streaming.domain.repositories.stream_repository import StreamRepository
from shared_kernel.infrastructure.persistence.postgresql_repository import PostgreSQLRepository


class StreamRepositoryPostgreSQL(PostgreSQLRepository[Stream], StreamRepository):
    """PostgreSQL implementation of StreamRepository."""
    
    async def save(self, entity: Stream) -> Stream:
        """Save stream to database."""
        async with self._transaction() as conn:
            await conn.execute(
                """
                INSERT INTO streams (id, camera_id, source_url, status, started_at, stopped_at, created_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT (id) DO UPDATE SET
                    status = EXCLUDED.status,
                    stopped_at = EXCLUDED.stopped_at
                """,
                entity.id,
                entity.camera_id,
                entity.source_url,
                entity.status.value,
                entity.started_at,
                entity.stopped_at,
                datetime.now()
            )
        return entity
    
    async def find_by_id(self, id: UUID) -> Optional[Stream]:
        """Find stream by ID."""
        async with self._connection() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM streams WHERE id = $1",
                id
            )
            
            if not row:
                return None
            
            return Stream(
                id=row['id'],
                camera_id=row['camera_id'],
                source_url=row['source_url'],
                status=StreamStatus(row['status']),
                started_at=row['started_at'],
                stopped_at=row['stopped_at']
            )
    
    async def find_by_camera_id(self, camera_id: UUID) -> Optional[Stream]:
        """Find active stream by camera ID."""
        async with self._connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT * FROM streams 
                WHERE camera_id = $1 AND status = $2
                ORDER BY created_at DESC
                LIMIT 1
                """,
                camera_id,
                StreamStatus.RUNNING.value
            )
            
            if not row:
                return None
            
            return Stream(
                id=row['id'],
                camera_id=row['camera_id'],
                source_url=row['source_url'],
                status=StreamStatus(row['status']),
                started_at=row['started_at'],
                stopped_at=row['stopped_at']
            )
    
    async def list_active(self) -> List[Stream]:
        """List all active streams."""
        async with self._connection() as conn:
            rows = await conn.fetch(
                "SELECT * FROM streams WHERE status = $1",
                StreamStatus.RUNNING.value
            )
            
            return [
                Stream(
                    id=row['id'],
                    camera_id=row['camera_id'],
                    source_url=row['source_url'],
                    status=StreamStatus(row['status']),
                    started_at=row['started_at'],
                    stopped_at=row['stopped_at']
                )
                for row in rows
            ]
    
    async def delete(self, id: UUID) -> None:
        """Delete stream by ID."""
        async with self._transaction() as conn:
            await conn.execute(
                "DELETE FROM streams WHERE id = $1",
                id
            )
    
    async def find_all(self) -> List[Stream]:
        """Find all streams."""
        async with self._connection() as conn:
            rows = await conn.fetch("SELECT * FROM streams")
            
            return [
                Stream(
                    id=row['id'],
                    camera_id=row['camera_id'],
                    source_url=row['source_url'],
                    status=StreamStatus(row['status']),
                    started_at=row['started_at'],
                    stopped_at=row['stopped_at']
                )
                for row in rows
            ]
