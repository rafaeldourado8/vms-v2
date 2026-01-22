"""FastAPI application for Streaming."""
from typing import Annotated
from fastapi import FastAPI, HTTPException, status, Query, Response, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest
from uuid import UUID
from datetime import datetime
from src.streaming.application.dtos.start_stream_dto import StartStreamDTO
from src.streaming.application.dtos.start_recording_dto import StartRecordingDTO
from src.streaming.application.dtos.search_recordings_dto import SearchRecordingsDTO
from src.streaming.application.dtos.get_timeline_dto import GetTimelineDTO
from src.streaming.application.dtos.generate_thumbnails_dto import GenerateThumbnailsDTO
from src.streaming.application.dtos.create_clip_dto import CreateClipDTO
from src.streaming.application.dtos.create_mosaic_dto import CreateMosaicDTO
from src.streaming.application.dtos.update_mosaic_dto import UpdateMosaicDTO
from src.streaming.application.use_cases.start_stream import StartStreamUseCase
from src.streaming.application.use_cases.stop_stream import StopStreamUseCase
from src.streaming.application.use_cases.start_recording import StartRecordingUseCase
from src.streaming.application.use_cases.stop_recording import StopRecordingUseCase
from src.streaming.application.use_cases.search_recordings import SearchRecordingsUseCase
from src.streaming.application.use_cases.get_timeline import GetTimelineUseCase
from src.streaming.application.use_cases.generate_thumbnails import GenerateThumbnailsUseCase
from src.streaming.application.use_cases.get_playback_url import GetPlaybackUrlUseCase
from src.streaming.application.use_cases.create_clip import CreateClipUseCase
from src.streaming.application.use_cases.create_mosaic import CreateMosaicUseCase
from src.streaming.application.use_cases.update_mosaic import UpdateMosaicUseCase
from src.streaming.infrastructure.persistence.stream_repository_impl import StreamRepositoryImpl
from src.streaming.infrastructure.persistence.recording_repository_impl import RecordingRepositoryImpl
from src.streaming.infrastructure.persistence.clip_repository_impl import ClipRepositoryImpl
from src.streaming.infrastructure.persistence.mosaic_repository_impl import MosaicRepositoryImpl
from src.streaming.infrastructure.external_services.mediamtx_client_impl import MediaMTXClientImpl
from src.streaming.infrastructure.external_services.thumbnail_service_impl import ThumbnailServiceImpl
from src.streaming.infrastructure.external_services.storage_service_impl import MinIOStorageService
from src.streaming.infrastructure.web.auth_routes import router as auth_router
from src.streaming.infrastructure.web.lgpd_routes import router as lgpd_router
from src.streaming.infrastructure.web.middleware import LoggingMiddleware
from src.shared_kernel.infrastructure.message_broker import MessageBroker
from src.shared_kernel.infrastructure.observability import prometheus_middleware
from src.shared_kernel.infrastructure.security.dependencies import User, get_current_user, require_permission
from src.shared_kernel.infrastructure.security.rbac import Permission
from src.shared_kernel.infrastructure.security.rate_limiter import limiter, rate_limit_exceeded_handler
from src.shared_kernel.infrastructure.logging_config import setup_logging
from slowapi.errors import RateLimitExceeded
import os

# Setup structured logging
setup_logging("streaming")

app = FastAPI(
    title="GT-Vision Streaming API",
    version="1.0.0",
    description="""
    🎥 **GT-Vision VMS** - Sistema de Gerenciamento de Vídeo Enterprise
    
    API para gerenciamento de streams, gravações, clipes e mosaicos de câmeras.
    
    ## Funcionalidades
    
    * **Streams** - Ingestão RTSP e distribuição HLS/WebRTC
    * **Gravações** - Gravação cíclica 24/7 com retenção configurável
    * **Timeline** - Navegação e playback de gravações
    * **Clipes** - Criação de clipes de vídeo
    * **Mosaicos** - Visualização de múltiplas câmeras
    
    ## Observabilidade
    
    * **Métricas**: `/metrics` - Prometheus metrics
    * **Health**: `/health` - Health check
    """,
    contact={
        "name": "GT-Vision Team",
        "email": "support@gtvision.com",
    },
    license_info={
        "name": "Proprietary",
    },
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
app.add_middleware(LoggingMiddleware)

# Prometheus middleware
app.middleware("http")(prometheus_middleware)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Auth routes
app.include_router(auth_router)

# LGPD routes
app.include_router(lgpd_router)

# Repositories and services
stream_repository = StreamRepositoryImpl()
recording_repository = RecordingRepositoryImpl()
clip_repository = ClipRepositoryImpl()
mosaic_repository = MosaicRepositoryImpl()
mediamtx_client = MediaMTXClientImpl()

# MessageBroker with RabbitMQ URL
rabbitmq_url = os.getenv(
    "RABBITMQ_URL",
    f"amqp://{os.getenv('RABBITMQ_USER', 'gtvision')}:{os.getenv('RABBITMQ_PASSWORD', 'gtvision_password')}@{os.getenv('RABBITMQ_HOST', 'rabbitmq')}:{os.getenv('RABBITMQ_PORT', '5672')}/"
)
message_broker = MessageBroker(rabbitmq_url)

thumbnail_service = ThumbnailServiceImpl()
storage_service = MinIOStorageService()


@app.post("/api/streams/start", status_code=status.HTTP_201_CREATED, tags=["Streams"], summary="Iniciar stream")
async def start_stream(
    dto: StartStreamDTO,
    user: Annotated[User, Depends(require_permission(Permission.WRITE_STREAMS))]
):
    """Inicia um novo stream RTSP de uma câmera.
    
    - **camera_id**: ID da câmera
    - **source_url**: URL RTSP da câmera (ex: rtsp://camera:554/stream)
    """
    try:
        use_case = StartStreamUseCase(stream_repository, mediamtx_client)
        result = await use_case.execute(dto)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/streams/{stream_id}/stop", status_code=status.HTTP_204_NO_CONTENT, tags=["Streams"], summary="Parar stream")
async def stop_stream(
    stream_id: UUID,
    user: Annotated[User, Depends(require_permission(Permission.WRITE_STREAMS))]
):
    """Para um stream ativo."""
    try:
        use_case = StopStreamUseCase(stream_repository, mediamtx_client)
        await use_case.execute(stream_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/streams/{stream_id}", tags=["Streams"], summary="Obter stream")
async def get_stream(
    stream_id: UUID,
    user: Annotated[User, Depends(require_permission(Permission.READ_STREAMS))]
):
    """Obtém informações de um stream."""
    stream = await stream_repository.find_by_id(stream_id)
    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")
    
    return {
        "id": str(stream.id),
        "camera_id": str(stream.camera_id),
        "source_url": stream.source_url,
        "status": stream.status.value,
        "started_at": stream.started_at.isoformat() if stream.started_at else None,
        "stopped_at": stream.stopped_at.isoformat() if stream.stopped_at else None
    }


@app.post("/api/recordings/start", status_code=status.HTTP_201_CREATED, tags=["Gravações"], summary="Iniciar gravação")
async def start_recording(
    dto: StartRecordingDTO,
    user: Annotated[User, Depends(require_permission(Permission.WRITE_RECORDINGS))]
):
    """Inicia gravação de um stream.
    
    - **stream_id**: ID do stream
    - **retention_days**: Dias de retenção (7, 15 ou 30)
    """
    try:
        use_case = StartRecordingUseCase(recording_repository, stream_repository, message_broker)
        result = await use_case.execute(dto)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/recordings/{recording_id}/stop", status_code=status.HTTP_204_NO_CONTENT, tags=["Gravações"], summary="Parar gravação")
async def stop_recording(
    recording_id: UUID,
    user: Annotated[User, Depends(require_permission(Permission.WRITE_RECORDINGS))]
):
    """Para uma gravação ativa."""
    try:
        use_case = StopRecordingUseCase(recording_repository, message_broker)
        await use_case.execute(recording_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/recordings/{recording_id}", tags=["Gravações"], summary="Obter gravação")
async def get_recording(
    recording_id: UUID,
    user: Annotated[User, Depends(require_permission(Permission.READ_RECORDINGS))]
):
    """Obtém informações de uma gravação."""
    recording = await recording_repository.find_by_id(recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    return {
        "recording_id": str(recording.id),
        "stream_id": str(recording.stream_id),
        "status": recording.status.value,
        "started_at": recording.started_at.isoformat(),
        "stopped_at": recording.stopped_at.isoformat() if recording.stopped_at else None,
        "retention_days": recording.retention_policy.days,
        "storage_path": recording.storage_path,
        "file_size_mb": recording.file_size_mb,
        "duration_seconds": recording.duration_seconds
    }


@app.get("/api/recordings/search", tags=["Gravações"], summary="Buscar gravações")
async def search_recordings(
    dto: SearchRecordingsDTO,
    user: Annotated[User, Depends(require_permission(Permission.READ_RECORDINGS))]
):
    """Busca gravações por filtros."""
    try:
        use_case = SearchRecordingsUseCase(recording_repository)
        results = await use_case.execute(dto)
        return {"recordings": [r.model_dump() for r in results], "total": len(results)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/timeline", tags=["Timeline"], summary="Obter timeline")
async def get_timeline(
    stream_id: UUID = Query(..., description="ID do stream"),
    start_date: datetime = Query(..., description="Data inicial"),
    end_date: datetime = Query(..., description="Data final")
):
    """Obtém timeline de gravações com segmentos e gaps."""
    try:
        dto = GetTimelineDTO(stream_id=stream_id, start_date=start_date, end_date=end_date)
        use_case = GetTimelineUseCase(recording_repository)
        result = await use_case.execute(dto)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/recordings/{recording_id}/thumbnails", tags=["Timeline"], summary="Gerar thumbnails")
async def generate_thumbnails(recording_id: UUID, dto: GenerateThumbnailsDTO):
    """Gera thumbnails de uma gravação."""
    try:
        dto.recording_id = recording_id
        use_case = GenerateThumbnailsUseCase(recording_repository, thumbnail_service)
        results = await use_case.execute(dto)
        return {"thumbnails": [r.model_dump() for r in results]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/recordings/{recording_id}/playback", tags=["Timeline"], summary="Obter URL de playback")
async def get_playback_url(recording_id: UUID):
    """Obtém URL presigned para playback de gravação."""
    try:
        use_case = GetPlaybackUrlUseCase(recording_repository, storage_service)
        result = await use_case.execute(recording_id)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/clips", status_code=status.HTTP_201_CREATED, tags=["Clipes"], summary="Criar clipe")
async def create_clip(dto: CreateClipDTO):
    """Cria um clipe de vídeo a partir de uma gravação.
    
    - **recording_id**: ID da gravação
    - **start_time**: Início do clipe
    - **end_time**: Fim do clipe
    """
    try:
        use_case = CreateClipUseCase(clip_repository, recording_repository, message_broker)
        result = await use_case.execute(dto)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/clips/{clip_id}", tags=["Clipes"], summary="Obter clipe")
async def get_clip(clip_id: UUID):
    """Obtém informações de um clipe."""
    clip = await clip_repository.find_by_id(clip_id)
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")
    
    return {
        "clip_id": str(clip.id),
        "recording_id": str(clip.recording_id),
        "start_time": clip.start_time.isoformat(),
        "end_time": clip.end_time.isoformat(),
        "status": clip.status.value,
        "storage_path": clip.storage_path,
        "file_size_mb": clip.file_size_mb,
        "duration_seconds": clip.duration_seconds,
        "created_at": clip.created_at.isoformat()
    }


@app.get("/api/clips/{clip_id}/download", tags=["Clipes"], summary="Download clipe")
async def download_clip(clip_id: UUID):
    """Faz download de um clipe em formato MP4."""
    clip = await clip_repository.find_by_id(clip_id)
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")
    
    if not clip.storage_path:
        raise HTTPException(status_code=400, detail="Clip not ready for download")
    
    return FileResponse(clip.storage_path, media_type="video/mp4", filename=f"clip_{clip_id}.mp4")


@app.post("/api/mosaics", status_code=status.HTTP_201_CREATED, tags=["Mosaicos"], summary="Criar mosaico")
async def create_mosaic(dto: CreateMosaicDTO):
    """Cria um mosaico de câmeras (máx 4)."""
    try:
        use_case = CreateMosaicUseCase(mosaic_repository)
        result = await use_case.execute(dto)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/mosaics/{mosaic_id}", tags=["Mosaicos"], summary="Obter mosaico")
async def get_mosaic(mosaic_id: UUID):
    """Obtém informações de um mosaico."""
    mosaic = await mosaic_repository.find_by_id(mosaic_id)
    if not mosaic:
        raise HTTPException(status_code=404, detail="Mosaic not found")
    
    return {
        "mosaic_id": str(mosaic.id),
        "user_id": str(mosaic.user_id),
        "name": mosaic.name,
        "layout": mosaic.layout,
        "camera_ids": [str(cid) for cid in mosaic.camera_ids]
    }


@app.put("/api/mosaics/{mosaic_id}", tags=["Mosaicos"], summary="Atualizar mosaico")
async def update_mosaic(mosaic_id: UUID, dto: UpdateMosaicDTO):
    """Atualiza um mosaico existente."""
    try:
        dto.mosaic_id = mosaic_id
        use_case = UpdateMosaicUseCase(mosaic_repository)
        result = await use_case.execute(dto)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/mosaics/{mosaic_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Mosaicos"], summary="Deletar mosaico")
async def delete_mosaic(mosaic_id: UUID):
    """Deleta um mosaico."""
    success = await mosaic_repository.delete(mosaic_id)
    if not success:
        raise HTTPException(status_code=404, detail="Mosaic not found")


@app.get("/api/users/{user_id}/mosaics", tags=["Mosaicos"], summary="Listar mosaicos do usuário")
async def list_user_mosaics(user_id: UUID):
    """Lista todos os mosaicos de um usuário."""
    mosaics = await mosaic_repository.find_by_user_id(user_id)
    return {
        "mosaics": [
            {
                "mosaic_id": str(m.id),
                "name": m.name,
                "layout": m.layout,
                "camera_count": len(m.camera_ids)
            }
            for m in mosaics
        ]
    }


@app.get("/health", tags=["Sistema"], summary="Health check")
async def health():
    """Verifica se a API está saudável."""
    return {"status": "healthy"}


@app.get("/metrics", tags=["Sistema"], summary="Métricas Prometheus", include_in_schema=False)
async def metrics():
    """Endpoint de métricas para Prometheus."""
    return Response(content=generate_latest(), media_type="text/plain")
