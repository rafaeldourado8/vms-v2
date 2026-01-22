"""Clip repository PostgreSQL implementation."""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from streaming.domain.entities.clip import Clip
from streaming.domain.value_objects.clip_status import ClipStatus
from streaming.domain.repositories.clip_repository import ClipRepository
from shared_kernel.infrastructure.persistence.postgresql_repository import PostgreSQLRepository


class ClipRepositoryPostgreSQL(PostgreSQLRepository[Clip], ClipRepository):
    """PostgreSQL implementation of ClipRepository."""
    
    async def save(self, entity: Clip) -> Clip:
        """Save clip to database."""
        async with self._transaction() as conn:
            await conn.execute(
                """
                INSERT INTO clips (
                    id, recording_id, start_time, end_time, 
                    status, storage_path, file_size_mb, created_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ON CONFLICT (id) DO UPDATE SET
                    status = EXCLUDED.status,
                    storage_path = EXCLUDED.storage_path,
                    file_size_mb = EXCLUDED.file_size_mb
                """,
                entity.id,
                entity.recording_id,
                entity.start_time,
                entity.end_time,
                entity.status.value,
                entity.storage_path,
                entity.file_size_mb,
                datetime.now()
            )
        return entity
    
    async def find_by_id(self, id: UUID) -> Optional[Clip]:
        """Find clip by ID."""
        async with self._connection() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM clips WHERE id = $1",
                id
            )
            
            if not row:
                return None
            
            return Clip(
                id=row['id'],
                recording_id=row['recording_id'],
                start_time=row['start_time'],
                end_time=row['end_time'],
                status=ClipStatus(row['status']),
                storage_path=row['storage_path'],
                file_size_mb=float(row['file_size_mb']) if row['file_size_mb'] else 0.0
            )
    
    async def find_by_recording_id(self, recording_id: UUID) -> List[Clip]:
        """Find clips by recording ID."""
        async with self._connection() as conn:
            rows = await conn.fetch(
                "SELECT * FROM clips WHERE recording_id = $1 ORDER BY created_at DESC",
                recording_id
            )
            
            return [
                Clip(
                    id=row['id'],
                    recording_id=row['recording_id'],
                    start_time=row['start_time'],
                    end_time=row['end_time'],
                    status=ClipStatus(row['status']),
                    storage_path=row['storage_path'],
                    file_size_mb=float(row['file_size_mb']) if row['file_size_mb'] else 0.0
                )
                for row in rows
            ]
    
    async def list_by_status(self, status: ClipStatus) -> List[Clip]:
        """List clips by status."""
        async with self._connection() as conn:
            rows = await conn.fetch(
                "SELECT * FROM clips WHERE status = $1 ORDER BY created_at DESC",
                status.value
            )
            
            return [
                Clip(
                    id=row['id'],
                    recording_id=row['recording_id'],
                    start_time=row['start_time'],
                    end_time=row['end_time'],
                    status=ClipStatus(row['status']),
                    storage_path=row['storage_path'],
                    file_size_mb=float(row['file_size_mb']) if row['file_size_mb'] else 0.0
                )
                for row in rows
            ]
    
    async def find_pending(self) -> List[Clip]:
        """Find pending clips for processing."""
        return await self.list_by_status(ClipStatus.PENDING)
    
    async def delete(self, id: UUID) -> None:
        """Delete clip by ID."""
        async with self._transaction() as conn:
            await conn.execute(
                "DELETE FROM clips WHERE id = $1",
                id
            )
    
    async def find_all(self) -> List[Clip]:
        """Find all clips."""
        async with self._connection() as conn:
            rows = await conn.fetch("SELECT * FROM clips ORDER BY created_at DESC")
            
            return [
                Clip(
                    id=row['id'],
                    recording_id=row['recording_id'],
                    start_time=row['start_time'],
                    end_time=row['end_time'],
                    status=ClipStatus(row['status']),
                    storage_path=row['storage_path'],
                    file_size_mb=float(row['file_size_mb']) if row['file_size_mb'] else 0.0
                )
                for row in rows
            ]
