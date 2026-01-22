from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, IPvAnyAddress
from typing import Optional
from uuid import uuid4

from src.modules.cameras.domain.services.url_builder import UrlBuilderFactory
from src.modules.cameras.domain.services.health_service import CameraHealthService
from src.modules.streaming.infrastructure.external_services.mediamtx_client_impl import MediaMTXClientImpl


router = APIRouter(prefix="/cameras", tags=["cameras"])


class CreateCameraRequest(BaseModel):
    nome: str
    ip: str
    marca: str
    modelo: Optional[str] = None
    usuario: str
    senha: str
    channel: int = 1
    subtype: int = 0
    port: Optional[int] = None


class CameraResponse(BaseModel):
    id: str
    nome: str
    ip: str
    marca: str
    modelo: Optional[str]
    rtsp_url: str
    hls_url: str
    status: str
    tenant_id: str


health_service = CameraHealthService()
mediamtx_client = MediaMTXClientImpl()


@router.post("", response_model=CameraResponse, status_code=201)
async def create_camera(
    request: CreateCameraRequest,
    x_tenant_id: str = Header(...)
):
    """
    Cadastra nova câmera com Smart URL Builder.
    
    Fluxo:
    1. Gera URL RTSP automaticamente (Strategy Pattern)
    2. Testa conectividade
    3. Cria path no MediaMTX
    4. Persiste no banco (TODO: implementar repository)
    5. Retorna dados com HLS URL
    """
    
    # Gerar URL RTSP
    try:
        builder = UrlBuilderFactory.get_builder(request.marca)
        rtsp_url = builder.build(
            ip=request.ip,
            user=request.usuario,
            password=request.senha,
            channel=request.channel,
            subtype=request.subtype,
            port=request.port
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Testar conectividade
    health_check = await health_service.check_rtsp_connectivity(rtsp_url)
    if not health_check["online"]:
        raise HTTPException(
            status_code=503,
            detail=f"Camera offline: {health_check['error']}"
        )
    
    # Gerar IDs
    camera_id = str(uuid4())
    stream_id = f"{x_tenant_id}_{camera_id}_live"
    
    # Criar path no MediaMTX
    success = await mediamtx_client.start_stream(stream_id, rtsp_url)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create MediaMTX path")
    
    # TODO: Persistir no banco via repository
    
    # Retornar resposta
    return CameraResponse(
        id=camera_id,
        nome=request.nome,
        ip=request.ip,
        marca=request.marca,
        modelo=request.modelo,
        rtsp_url=rtsp_url,
        hls_url=f"http://localhost/stream/{stream_id}/index.m3u8",
        status="online",
        tenant_id=x_tenant_id
    )


@router.get("/{camera_id}/health")
async def check_camera_health(
    camera_id: str,
    x_tenant_id: str = Header(...)
):
    """Verifica status de conectividade da câmera."""
    # TODO: Buscar rtsp_url do banco
    # Por enquanto, retorna mock
    return {
        "camera_id": camera_id,
        "status": "online",
        "message": "Health check not fully implemented yet"
    }


@router.get("/brands")
async def list_supported_brands():
    """Lista marcas de câmeras suportadas."""
    return {
        "brands": UrlBuilderFactory.supported_brands()
    }
