from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.modules.cameras.infra.camera_routes import router as cameras_router
from src.modules.cameras.infra.webhooks import router as webhooks_router
from src.modules.streaming.infrastructure.web.mosaic_routes import router as mosaics_router
from src.modules.streaming.infrastructure.web.snapshot_routes import router as snapshots_router
from src.modules.streaming.infrastructure.web.auth_routes import router as auth_router
from src.modules.streaming.infrastructure.web.clip_routes import router as clips_router
from src.modules.streaming.infrastructure.web.report_routes import router as reports_router
from src.modules.streaming.infrastructure.web.websocket_routes import router as websocket_router
from src.modules.streaming.infrastructure.web.map_routes import router as map_router
from src.modules.streaming.infrastructure.web.dashboard_routes import router as dashboard_router
from src.modules.streaming.infrastructure.web.notification_routes import router as notification_router


app = FastAPI(
    title="GT-Vision VMS API",
    description="Sistema de Gerenciamento de Vídeo Enterprise",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(cameras_router, prefix="/api/v1")
app.include_router(webhooks_router, prefix="/api/v1")
app.include_router(mosaics_router, prefix="/api/v1")
app.include_router(snapshots_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(clips_router, prefix="/api/v1")
app.include_router(reports_router, prefix="/api/v1")
app.include_router(websocket_router)
app.include_router(map_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(notification_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "gtvision-streaming"}


@app.get("/")
async def root():
    return {
        "service": "GT-Vision VMS",
        "version": "2.0.0",
        "docs": "/docs"
    }
