"""Recording repository PostgreSQL implementation."""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from streaming.domain.entities.recording import Recording
from streaming.domain.value_objects.recording_status import RecordingStatus
from streaming.domain.value_objects.retention_policy import RetentionPolicy
from streaming.domain.repositories.recording_repository import RecordingRepository
from shared_kernel.infrastructure.persistence.postgresql_repository import PostgreSQLRepository


class RecordingRepositoryPostgreSQL(PostgreSQLRepository[Recording], RecordingRepository):
    """PostgreSQL implementation of RecordingRepository."""
    
    async def save(self, entity: Recording) -> Recording:
        """Save recording to database."""
        async with self._transaction() as conn:
            await conn.execute(
                """
                INSERT INTO recordings (
                    id, stream_id, retention_days, status, 
                    started_at, stopped_at, storage_path, 
                    file_size_mb, duration_seconds
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                ON CONFLICT (id) DO UPDATE SET
                    status = EXCLUDED.status,
                    stopped_at = EXCLUDED.stopped_at,
                    storage_path = EXCLUDED.storage_path,
                    file_size_mb = EXCLUDED.file_size_mb,
                    duration_seconds = EXCLUDED.duration_seconds
                """,
                entity.id,
                entity.stream_id,
                entity.retention_policy.days,
                entity.status.value,
                entity.started_at,
                entity.stopped_at,
                entity.storage_path,
                entity.file_size_mb,
                entity.duration_seconds
            )
        return entity
    
    async def find_by_id(self, id: UUID) -> Optional[Recording]:
        """Find recording by ID."""
        async with self._connection() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM recordings WHERE id = $1",
                id
            )
            
            if not row:
                return None
            
            return Recording(
                id=row['id'],
                stream_id=row['stream_id'],
                retention_policy=RetentionPolicy(row['retention_days']),
                status=RecordingStatus(row['status']),
                started_at=row['started_at'],
                stopped_at=row['stopped_at'],
                storage_path=row['storage_path'],
                file_size_mb=float(row['file_size_mb']) if row['file_size_mb'] else 0.0,
                duration_seconds=row['duration_seconds'] or 0
            )
    
    async def find_by_stream_id(self, stream_id: UUID) -> List[Recording]:
        """Find recordings by stream ID."""
        async with self._connection() as conn:
            rows = await conn.fetch(
                "SELECT * FROM recordings WHERE stream_id = $1 ORDER BY started_at DESC",
                stream_id
            )
            
            return [
                Recording(
                    id=row['id'],
                    stream_id=row['stream_id'],
                    retention_policy=RetentionPolicy(row['retention_days']),
                    status=RecordingStatus(row['status']),
                    started_at=row['started_at'],
                    stopped_at=row['stopped_at'],
                    storage_path=row['storage_path'],
                    file_size_mb=float(row['file_size_mb']) if row['file_size_mb'] else 0.0,
                    duration_seconds=row['duration_seconds'] or 0
                )
                for row in rows
            ]
    
    async def search(
        self,
        camera_id: Optional[UUID] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Recording]:
        """Search recordings with filters."""
        query = "SELECT * FROM recordings WHERE 1=1"
        params = []
        param_count = 1
        
        if start_date:
            query += f" AND started_at >= ${param_count}"
            params.append(start_date)
            param_count += 1
        
        if end_date:
            query += f" AND started_at <= ${param_count}"
            params.append(end_date)
            param_count += 1
        
        query += " ORDER BY started_at DESC"
        
        async with self._connection() as conn:
            rows = await conn.fetch(query, *params)
            
            return [
                Recording(
                    id=row['id'],
                    stream_id=row['stream_id'],
                    retention_policy=RetentionPolicy(row['retention_days']),
                    status=RecordingStatus(row['status']),
                    started_at=row['started_at'],
                    stopped_at=row['stopped_at'],
                    storage_path=row['storage_path'],
                    file_size_mb=float(row['file_size_mb']) if row['file_size_mb'] else 0.0,
                    duration_seconds=row['duration_seconds'] or 0
                )
                for row in rows
            ]
    
    async def delete(self, id: UUID) -> None:
        """Delete recording by ID."""
        async with self._transaction() as conn:
            await conn.execute(
                "DELETE FROM recordings WHERE id = $1",
                id
            )
    
    async def find_all(self) -> List[Recording]:
        """Find all recordings."""
        async with self._connection() as conn:
            rows = await conn.fetch("SELECT * FROM recordings ORDER BY started_at DESC")
            
            return [
                Recording(
                    id=row['id'],
                    stream_id=row['stream_id'],
                    retention_policy=RetentionPolicy(row['retention_days']),
                    status=RecordingStatus(row['status']),
                    started_at=row['started_at'],
                    stopped_at=row['stopped_at'],
                    storage_path=row['storage_path'],
                    file_size_mb=float(row['file_size_mb']) if row['file_size_mb'] else 0.0,
                    duration_seconds=row['duration_seconds'] or 0
                )
                for row in rows
            ]
    
    async def find_active_by_stream_id(self, stream_id: UUID) -> Optional[Recording]:
        """Find active recording by stream ID."""
        async with self._connection() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM recordings WHERE stream_id = $1 AND status = $2 LIMIT 1",
                stream_id,
                RecordingStatus.RECORDING.value
            )
            
            if not row:
                return None
            
            return Recording(
                id=row['id'],
                stream_id=row['stream_id'],
                retention_policy=RetentionPolicy(row['retention_days']),
                status=RecordingStatus(row['status']),
                started_at=row['started_at'],
                stopped_at=row['stopped_at'],
                storage_path=row['storage_path'],
                file_size_mb=float(row['file_size_mb']) if row['file_size_mb'] else 0.0,
                duration_seconds=row['duration_seconds'] or 0
            )
    
    async def find_expired(self) -> List[Recording]:
        """Find expired recordings."""
        async with self._connection() as conn:
            rows = await conn.fetch(
                "SELECT * FROM recordings WHERE stopped_at < NOW() - (retention_days || ' days')::INTERVAL"
            )
            
            return [
                Recording(
                    id=row['id'],
                    stream_id=row['stream_id'],
                    retention_policy=RetentionPolicy(row['retention_days']),
                    status=RecordingStatus(row['status']),
                    started_at=row['started_at'],
                    stopped_at=row['stopped_at'],
                    storage_path=row['storage_path'],
                    file_size_mb=float(row['file_size_mb']) if row['file_size_mb'] else 0.0,
                    duration_seconds=row['duration_seconds'] or 0
                )
                for row in rows
            ]

    async def count_active(self) -> int:
        """Count active recordings."""
        async with self._connection() as conn:
            row = await conn.fetchrow(
                "SELECT COUNT(*) as count FROM recordings WHERE status = $1",
                RecordingStatus.RECORDING.value
            )
            return row['count'] if row else 0
