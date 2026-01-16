"""LPR Event repository PostgreSQL implementation."""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from ai.domain.entities.lpr_event import LPREvent
from ai.domain.repositories.lpr_event_repository import LPREventRepository
from shared_kernel.infrastructure.persistence.postgresql_repository import PostgreSQLRepository


class LPREventRepositoryPostgreSQL(PostgreSQLRepository[LPREvent], LPREventRepository):
    """PostgreSQL implementation of LPREventRepository."""
    
    async def save(self, entity: LPREvent) -> LPREvent:
        """Save LPR event to database."""
        async with self._transaction() as conn:
            await conn.execute(
                """
                INSERT INTO lpr_events (
                    id, camera_id, plate, confidence, 
                    image_url, detected_at, city_id
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT (id) DO UPDATE SET
                    confidence = EXCLUDED.confidence,
                    image_url = EXCLUDED.image_url
                """,
                entity.id,
                entity.camera_id,
                entity.plate,
                entity.confidence,
                entity.image_url,
                entity.detected_at,
                entity.city_id
            )
        return entity
    
    async def find_by_id(self, id: UUID) -> Optional[LPREvent]:
        """Find LPR event by ID."""
        async with self._connection() as conn:
            row = await conn.fetchrow("SELECT * FROM lpr_events WHERE id = $1", id)
            
            if not row:
                return None
            
            return LPREvent(
                id=row['id'],
                camera_id=row['camera_id'],
                plate=row['plate'],
                confidence=float(row['confidence']),
                image_url=row['image_url'],
                detected_at=row['detected_at'],
                city_id=row['city_id']
            )
    
    async def search(
        self,
        plate: Optional[str] = None,
        camera_id: Optional[UUID] = None,
        city_id: Optional[UUID] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[LPREvent]:
        """Search LPR events by filters."""
        query = "SELECT * FROM lpr_events WHERE 1=1"
        params = []
        param_count = 1
        
        if plate:
            query += f" AND plate ILIKE ${param_count}"
            params.append(f"%{plate.upper()}%")
            param_count += 1
        
        if camera_id:
            query += f" AND camera_id = ${param_count}"
            params.append(camera_id)
            param_count += 1
        
        if city_id:
            query += f" AND city_id = ${param_count}"
            params.append(city_id)
            param_count += 1
        
        if start_date:
            query += f" AND detected_at >= ${param_count}"
            params.append(start_date)
            param_count += 1
        
        if end_date:
            query += f" AND detected_at <= ${param_count}"
            params.append(end_date)
            param_count += 1
        
        query += " ORDER BY detected_at DESC"
        
        async with self._connection() as conn:
            rows = await conn.fetch(query, *params)
            
            return [
                LPREvent(
                    id=row['id'],
                    camera_id=row['camera_id'],
                    plate=row['plate'],
                    confidence=float(row['confidence']),
                    image_url=row['image_url'],
                    detected_at=row['detected_at'],
                    city_id=row['city_id']
                )
                for row in rows
            ]
    
    async def find_by_plate(self, plate: str) -> List[LPREvent]:
        """Find events by plate."""
        async with self._connection() as conn:
            rows = await conn.fetch(
                "SELECT * FROM lpr_events WHERE plate = $1 ORDER BY detected_at DESC",
                plate.upper()
            )
            
            return [
                LPREvent(
                    id=row['id'],
                    camera_id=row['camera_id'],
                    plate=row['plate'],
                    confidence=float(row['confidence']),
                    image_url=row['image_url'],
                    detected_at=row['detected_at'],
                    city_id=row['city_id']
                )
                for row in rows
            ]
    
    async def delete(self, id: UUID) -> None:
        """Delete LPR event by ID."""
        async with self._transaction() as conn:
            await conn.execute("DELETE FROM lpr_events WHERE id = $1", id)
    
    async def find_all(self) -> List[LPREvent]:
        """Find all LPR events."""
        async with self._connection() as conn:
            rows = await conn.fetch("SELECT * FROM lpr_events ORDER BY detected_at DESC")
            
            return [
                LPREvent(
                    id=row['id'],
                    camera_id=row['camera_id'],
                    plate=row['plate'],
                    confidence=float(row['confidence']),
                    image_url=row['image_url'],
                    detected_at=row['detected_at'],
                    city_id=row['city_id']
                )
                for row in rows
            ]
