from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
from enum import Enum


router = APIRouter(prefix="/mosaics", tags=["mosaics"])


class LayoutType(str, Enum):
    GRID_2X2 = "2x2"
    GRID_4X4 = "4x4"
    GRID_3X3 = "3x3"


class CreateMosaicRequest(BaseModel):
    nome: str
    layout: LayoutType
    cameras: list[str]


class MosaicResponse(BaseModel):
    id: str
    nome: str
    layout: LayoutType
    cameras: list[dict]
    tenant_id: str


# Mock storage (TODO: implementar repository)
mosaics_db = {}


@router.post("", response_model=MosaicResponse, status_code=201)
async def create_mosaic(
    request: CreateMosaicRequest,
    x_tenant_id: str = Header(...)
):
    """Cria mosaico de câmeras."""
    
    # Validar número de câmeras
    max_cameras = {"2x2": 4, "3x3": 9, "4x4": 16}
    if len(request.cameras) > max_cameras[request.layout]:
        raise HTTPException(
            status_code=400,
            detail=f"Layout {request.layout} suporta no máximo {max_cameras[request.layout]} câmeras"
        )
    
    mosaic_id = str(uuid4())
    
    # TODO: Buscar dados das câmeras do banco
    cameras_data = [
        {
            "id": cam_id,
            "hls_url": f"http://localhost/stream/{x_tenant_id}_{cam_id}_live/index.m3u8",
            "position": idx
        }
        for idx, cam_id in enumerate(request.cameras)
    ]
    
    mosaic = {
        "id": mosaic_id,
        "nome": request.nome,
        "layout": request.layout,
        "cameras": cameras_data,
        "tenant_id": x_tenant_id
    }
    
    mosaics_db[mosaic_id] = mosaic
    
    return MosaicResponse(**mosaic)


@router.get("/{mosaic_id}", response_model=MosaicResponse)
async def get_mosaic(
    mosaic_id: str,
    x_tenant_id: str = Header(...)
):
    """Obtém mosaico por ID."""
    mosaic = mosaics_db.get(mosaic_id)
    
    if not mosaic:
        raise HTTPException(status_code=404, detail="Mosaic not found")
    
    if mosaic["tenant_id"] != x_tenant_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    return MosaicResponse(**mosaic)


@router.patch("/{mosaic_id}", response_model=MosaicResponse)
async def update_mosaic(
    mosaic_id: str,
    request: CreateMosaicRequest,
    x_tenant_id: str = Header(...)
):
    """Atualiza layout do mosaico."""
    mosaic = mosaics_db.get(mosaic_id)
    
    if not mosaic:
        raise HTTPException(status_code=404, detail="Mosaic not found")
    
    if mosaic["tenant_id"] != x_tenant_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # Atualizar
    mosaic["nome"] = request.nome
    mosaic["layout"] = request.layout
    mosaic["cameras"] = [
        {
            "id": cam_id,
            "hls_url": f"http://localhost/stream/{x_tenant_id}_{cam_id}_live/index.m3u8",
            "position": idx
        }
        for idx, cam_id in enumerate(request.cameras)
    ]
    
    return MosaicResponse(**mosaic)


@router.delete("/{mosaic_id}", status_code=204)
async def delete_mosaic(
    mosaic_id: str,
    x_tenant_id: str = Header(...)
):
    """Remove mosaico."""
    mosaic = mosaics_db.get(mosaic_id)
    
    if not mosaic:
        raise HTTPException(status_code=404, detail="Mosaic not found")
    
    if mosaic["tenant_id"] != x_tenant_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    del mosaics_db[mosaic_id]
    return None
