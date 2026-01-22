from fastapi import APIRouter, Header
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, text

router = APIRouter(prefix="/map", tags=["map"])

engine = create_engine('postgresql://gtvision:gtvision_password@postgres:5432/gtvision')


class CameraLocation(BaseModel):
    camera_id: str
    latitude: float
    longitude: float
    nome: str
    status: str


class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: dict
    properties: dict


class GeoJSONResponse(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]


@router.get("/cameras", response_model=GeoJSONResponse)
async def get_cameras_geojson(
    x_tenant_id: str = Header(...)
):
    """
    Retorna câmeras do tenant em formato GeoJSON para plotagem em mapa.
    
    Compatível com Leaflet, Mapbox, Google Maps.
    """
    
    with engine.connect() as conn:
        query = text("""
            SELECT 
                c.id,
                c.nome,
                c.latitude,
                c.longitude,
                c.status,
                c.ip,
                c.marca,
                c.modelo,
                COUNT(d.id) as detections_24h
            FROM cameras c
            LEFT JOIN deteccoes d ON d.camera_id = c.id 
                AND d.timestamp > NOW() - INTERVAL '24 hours'
            WHERE 
                c.tenant_id = :tenant_id
                AND c.latitude IS NOT NULL
                AND c.longitude IS NOT NULL
            GROUP BY c.id
        """)
        
        cameras = conn.execute(query, {"tenant_id": x_tenant_id}).fetchall()
        
        features = []
        for cam in cameras:
            # Cor do marcador baseado no status
            marker_color = {
                "online": "#28a745",
                "offline": "#dc3545",
                "warning": "#ffc107"
            }.get(cam.status, "#6c757d")
            
            feature = GeoJSONFeature(
                type="Feature",
                geometry={
                    "type": "Point",
                    "coordinates": [cam.longitude, cam.latitude]
                },
                properties={
                    "camera_id": cam.id,
                    "nome": cam.nome,
                    "status": cam.status,
                    "ip": cam.ip,
                    "marca": cam.marca,
                    "modelo": cam.modelo,
                    "detections_24h": cam.detections_24h,
                    "marker_color": marker_color,
                    "hls_url": f"http://localhost/stream/{x_tenant_id}_{cam.id}_live/index.m3u8"
                }
            )
            features.append(feature)
        
        return GeoJSONResponse(
            type="FeatureCollection",
            features=features
        )


@router.get("/heatmap")
async def get_detections_heatmap(
    x_tenant_id: str = Header(...),
    hours: int = 24
):
    """
    Retorna heatmap de detecções para visualização tática.
    
    Mostra concentração de eventos LPR por região.
    """
    
    with engine.connect() as conn:
        query = text("""
            SELECT 
                c.latitude,
                c.longitude,
                COUNT(d.id) as intensity
            FROM deteccoes d
            JOIN cameras c ON d.camera_id = c.id
            WHERE 
                d.tenant_id = :tenant_id
                AND d.timestamp > NOW() - (:hours || ' hours')::INTERVAL
                AND c.latitude IS NOT NULL
                AND c.longitude IS NOT NULL
            GROUP BY c.latitude, c.longitude
        """)
        
        points = conn.execute(query, {
            "tenant_id": x_tenant_id,
            "hours": hours
        }).fetchall()
        
        heatmap_data = [
            {
                "lat": point.latitude,
                "lng": point.longitude,
                "intensity": point.intensity
            }
            for point in points
        ]
        
        return {
            "type": "heatmap",
            "data": heatmap_data,
            "period_hours": hours
        }
