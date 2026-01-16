"""
GT-Vision Detection API - FastAPI separada para receber eventos de detecção.
Esta API é independente do Streaming API e recebe webhooks das câmeras.
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GT-Vision Detection API",
    version="1.0.0",
    description="API para receber eventos de detecção (LPR, objetos, etc) das câmeras"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LPREventDTO(BaseModel):
    camera_id: UUID
    plate: str = Field(..., min_length=7, max_length=8)
    confidence: float = Field(..., ge=0.0, le=1.0)
    timestamp: datetime
    image_url: Optional[str] = None
    location: Optional[str] = None


class ObjectDetectionEventDTO(BaseModel):
    camera_id: UUID
    object_type: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    timestamp: datetime
    bbox: Optional[dict] = None
    image_url: Optional[str] = None


lpr_events: List[dict] = []
object_events: List[dict] = []


@app.post("/api/webhooks/lpr", status_code=status.HTTP_201_CREATED, tags=["Webhooks"])
async def receive_lpr_event(event: LPREventDTO):
    logger.info(f"📸 LPR detectado: {event.plate} - Câmera: {event.camera_id}")
    
    event_data = {
        "id": str(uuid4()),
        "camera_id": str(event.camera_id),
        "plate": event.plate,
        "confidence": event.confidence,
        "timestamp": event.timestamp.isoformat(),
        "image_url": event.image_url,
        "location": event.location,
        "received_at": datetime.utcnow().isoformat()
    }
    
    lpr_events.append(event_data)
    
    return {
        "event_id": event_data["id"],
        "status": "received",
        "message": f"LPR event for plate {event.plate} received successfully"
    }


@app.post("/api/webhooks/object-detection", status_code=status.HTTP_201_CREATED, tags=["Webhooks"])
async def receive_object_detection_event(event: ObjectDetectionEventDTO):
    logger.info(f"🎯 Objeto detectado: {event.object_type} - Câmera: {event.camera_id}")
    
    event_data = {
        "id": str(uuid4()),
        "camera_id": str(event.camera_id),
        "object_type": event.object_type,
        "confidence": event.confidence,
        "timestamp": event.timestamp.isoformat(),
        "bbox": event.bbox,
        "image_url": event.image_url,
        "received_at": datetime.utcnow().isoformat()
    }
    
    object_events.append(event_data)
    
    return {
        "event_id": event_data["id"],
        "status": "received",
        "message": f"Object detection event for {event.object_type} received successfully"
    }


@app.get("/api/events/lpr", tags=["Events"])
async def list_lpr_events(
    camera_id: Optional[UUID] = None,
    plate: Optional[str] = None,
    limit: int = 100
):
    filtered = lpr_events
    
    if camera_id:
        filtered = [e for e in filtered if e["camera_id"] == str(camera_id)]
    
    if plate:
        filtered = [e for e in filtered if plate.upper() in e["plate"].upper()]
    
    return {"events": filtered[:limit], "total": len(filtered)}


@app.get("/api/events/objects", tags=["Events"])
async def list_object_events(
    camera_id: Optional[UUID] = None,
    object_type: Optional[str] = None,
    limit: int = 100
):
    filtered = object_events
    
    if camera_id:
        filtered = [e for e in filtered if e["camera_id"] == str(camera_id)]
    
    if object_type:
        filtered = [e for e in filtered if e["object_type"] == object_type]
    
    return {"events": filtered[:limit], "total": len(filtered)}


@app.get("/api/events/lpr/{event_id}", tags=["Events"])
async def get_lpr_event(event_id: str):
    event = next((e for e in lpr_events if e["id"] == event_id), None)
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return event


@app.delete("/api/events/lpr", tags=["Events"])
async def clear_lpr_events():
    lpr_events.clear()
    return {"message": "All LPR events cleared"}


@app.delete("/api/events/objects", tags=["Events"])
async def clear_object_events():
    object_events.clear()
    return {"message": "All object detection events cleared"}


@app.get("/health", tags=["Sistema"])
async def health():
    return {
        "status": "healthy",
        "service": "detection-api",
        "lpr_events_count": len(lpr_events),
        "object_events_count": len(object_events)
    }


@app.get("/", tags=["Sistema"])
async def root():
    return {
        "service": "GT-Vision Detection API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
