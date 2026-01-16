"""FastAPI application for AI Context."""
from fastapi import FastAPI, HTTPException, status, Query
from uuid import UUID
from datetime import datetime
from typing import Optional
from src.ai.application.dtos.receive_lpr_event_dto import ReceiveLPREventDTO
from src.ai.application.dtos.search_lpr_events_dto import SearchLPREventsDTO
from src.ai.application.use_cases.receive_lpr_event import ReceiveLPREventUseCase
from src.ai.application.use_cases.search_lpr_events import SearchLPREventsUseCase
from src.ai.infrastructure.persistence.lpr_event_repository_impl import LPREventRepositoryImpl
from src.streaming.infrastructure.external_services.storage_service_impl import MinIOStorageService

app = FastAPI(title="GT-Vision AI API", version="1.0.0")

lpr_event_repository = LPREventRepositoryImpl()
storage_service = MinIOStorageService()


@app.post("/api/lpr/events", status_code=status.HTTP_201_CREATED)
async def receive_lpr_event(dto: ReceiveLPREventDTO):
    """Receive LPR event webhook."""
    try:
        use_case = ReceiveLPREventUseCase(lpr_event_repository, storage_service)
        result = await use_case.execute(dto)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/lpr/events")
async def search_lpr_events(
    plate: Optional[str] = Query(None),
    camera_id: Optional[UUID] = Query(None),
    city_id: Optional[UUID] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None)
):
    """Search LPR events."""
    try:
        dto = SearchLPREventsDTO(
            plate=plate,
            camera_id=camera_id,
            city_id=city_id,
            start_date=start_date,
            end_date=end_date
        )
        use_case = SearchLPREventsUseCase(lpr_event_repository)
        results = await use_case.execute(dto)
        return {"events": [r.model_dump() for r in results], "total": len(results)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/lpr/events/{event_id}")
async def get_lpr_event(event_id: UUID):
    """Get LPR event by ID."""
    event = await lpr_event_repository.find_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return {
        "event_id": str(event.id),
        "camera_id": str(event.camera_id),
        "plate": event.plate,
        "confidence": event.confidence,
        "image_url": event.image_url,
        "detected_at": event.detected_at.isoformat(),
        "city_id": str(event.city_id) if event.city_id else None
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
