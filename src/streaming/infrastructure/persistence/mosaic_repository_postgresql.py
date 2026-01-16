"""Mosaic repository PostgreSQL implementation."""
from typing import List, Optional
from uuid import UUID
import json

from streaming.domain.entities.mosaic import Mosaic
from streaming.domain.repositories.mosaic_repository import MosaicRepository
from shared_kernel.infrastructure.persistence.postgresql_repository import PostgreSQLRepository


class MosaicRepositoryPostgreSQL(PostgreSQLRepository[Mosaic], MosaicRepository):
    """PostgreSQL implementation of MosaicRepository."""
    
    async def save(self, entity: Mosaic) -> Mosaic:
        """Save mosaic to database."""
        async with self._transaction() as conn:
            await conn.execute(
                """
                INSERT INTO mosaics (id, user_id, name, layout, camera_ids)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    layout = EXCLUDED.layout,
                    camera_ids = EXCLUDED.camera_ids
                """,
                entity.id,
                entity.user_id,
                entity.name,
                entity.layout,
                json.dumps([str(cid) for cid in entity.camera_ids])
            )
        return entity
    
    async def find_by_id(self, id: UUID) -> Optional[Mosaic]:
        """Find mosaic by ID."""
        async with self._connection() as conn:
            row = await conn.fetchrow("SELECT * FROM mosaics WHERE id = $1", id)
            
            if not row:
                return None
            
            camera_ids = [UUID(cid) for cid in json.loads(row['camera_ids'])] if row['camera_ids'] else []
            
            return Mosaic(
                id=row['id'],
                user_id=row['user_id'],
                name=row['name'],
                layout=row['layout'],
                camera_ids=camera_ids
            )
    
    async def find_by_user_id(self, user_id: UUID) -> List[Mosaic]:
        """Find mosaics by user ID."""
        async with self._connection() as conn:
            rows = await conn.fetch(
                "SELECT * FROM mosaics WHERE user_id = $1 ORDER BY created_at DESC",
                user_id
            )
            
            return [
                Mosaic(
                    id=row['id'],
                    user_id=row['user_id'],
                    name=row['name'],
                    layout=row['layout'],
                    camera_ids=[UUID(cid) for cid in json.loads(row['camera_ids'])] if row['camera_ids'] else []
                )
                for row in rows
            ]
    
    async def delete(self, id: UUID) -> None:
        """Delete mosaic by ID."""
        async with self._transaction() as conn:
            await conn.execute("DELETE FROM mosaics WHERE id = $1", id)
    
    async def find_all(self) -> List[Mosaic]:
        """Find all mosaics."""
        async with self._connection() as conn:
            rows = await conn.fetch("SELECT * FROM mosaics ORDER BY created_at DESC")
            
            return [
                Mosaic(
                    id=row['id'],
                    user_id=row['user_id'],
                    name=row['name'],
                    layout=row['layout'],
                    camera_ids=[UUID(cid) for cid in json.loads(row['camera_ids'])] if row['camera_ids'] else []
                )
                for row in rows
            ]
