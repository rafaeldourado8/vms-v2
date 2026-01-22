from fastapi import APIRouter, Header
from pydantic import BaseModel
from typing import List, Dict
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import httpx

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

engine = create_engine('postgresql://gtvision:gtvision_password@postgres:5432/gtvision')


class CameraHealthStatus(BaseModel):
    camera_id: str
    nome: str
    status: str
    last_seen: str
    recording_status: str


class DashboardMetrics(BaseModel):
    cameras_online: int
    cameras_offline: int
    cameras_warning: int
    total_cameras: int
    detections_24h: int
    storage_used_gb: float
    storage_total_gb: float
    storage_percent: float
    recording_failures_24h: int


class SystemHealth(BaseModel):
    service: str
    status: str
    message: str


@router.get("/health", response_model=Dict)
async def get_dashboard_health(
    x_tenant_id: str = Header(...)
):
    """
    Dashboard de saúde completo do sistema.
    
    Retorna:
    - Status de câmeras (online/offline/warning)
    - Métricas de detecções
    - Uso de storage
    - Falhas de gravação
    - Status de serviços
    """
    
    with engine.connect() as conn:
        # Métricas de câmeras
        cameras_query = text("""
            SELECT 
                status,
                COUNT(*) as count
            FROM cameras
            WHERE tenant_id = :tenant_id
            GROUP BY status
        """)
        cameras_status = conn.execute(cameras_query, {"tenant_id": x_tenant_id}).fetchall()
        
        status_counts = {row.status: row.count for row in cameras_status}
        total_cameras = sum(status_counts.values())
        
        # Detecções 24h
        detections_query = text("""
            SELECT COUNT(*) as count
            FROM deteccoes
            WHERE 
                tenant_id = :tenant_id
                AND timestamp > NOW() - INTERVAL '24 hours'
        """)
        detections_count = conn.execute(detections_query, {"tenant_id": x_tenant_id}).scalar()
        
        # Storage
        storage_query = text("""
            SELECT 
                COALESCE(SUM(size_bytes), 0) as used_bytes
            FROM recordings
            WHERE 
                tenant_id = :tenant_id
                AND deleted_at IS NULL
        """)
        storage_used = conn.execute(storage_query, {"tenant_id": x_tenant_id}).scalar()
        
        # Plano do tenant
        plan_query = text("""
            SELECT p.storage_limit_gb
            FROM cidades c
            JOIN planos p ON c.plano_id = p.id
            WHERE c.id = :tenant_id
        """)
        plan = conn.execute(plan_query, {"tenant_id": x_tenant_id}).fetchone()
        storage_total_gb = plan.storage_limit_gb if plan else 1000
        
        # Falhas de gravação
        failures_query = text("""
            SELECT COUNT(*) as count
            FROM audit_logs
            WHERE 
                tenant_id = :tenant_id
                AND action = 'recording.failed'
                AND created_at > NOW() - INTERVAL '24 hours'
        """)
        failures_count = conn.execute(failures_query, {"tenant_id": x_tenant_id}).scalar()
    
    # Verificar serviços externos
    services_health = await check_services_health()
    
    metrics = DashboardMetrics(
        cameras_online=status_counts.get("online", 0),
        cameras_offline=status_counts.get("offline", 0),
        cameras_warning=status_counts.get("warning", 0),
        total_cameras=total_cameras,
        detections_24h=detections_count or 0,
        storage_used_gb=round((storage_used or 0) / (1024**3), 2),
        storage_total_gb=storage_total_gb,
        storage_percent=round(((storage_used or 0) / (storage_total_gb * 1024**3)) * 100, 2),
        recording_failures_24h=failures_count or 0
    )
    
    return {
        "metrics": metrics,
        "services": services_health,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/cameras/status", response_model=List[CameraHealthStatus])
async def get_cameras_status(
    x_tenant_id: str = Header(...)
):
    """Lista status detalhado de todas as câmeras."""
    
    with engine.connect() as conn:
        query = text("""
            SELECT 
                c.id,
                c.nome,
                c.status,
                c.last_seen,
                CASE 
                    WHEN r.id IS NOT NULL THEN 'recording'
                    ELSE 'idle'
                END as recording_status
            FROM cameras c
            LEFT JOIN recordings r ON r.camera_id = c.id 
                AND r.end_time IS NULL
            WHERE c.tenant_id = :tenant_id
            ORDER BY c.status DESC, c.nome
        """)
        
        cameras = conn.execute(query, {"tenant_id": x_tenant_id}).fetchall()
        
        return [
            CameraHealthStatus(
                camera_id=cam.id,
                nome=cam.nome,
                status=cam.status,
                last_seen=cam.last_seen.isoformat() if cam.last_seen else "never",
                recording_status=cam.recording_status
            )
            for cam in cameras
        ]


async def check_services_health() -> List[SystemHealth]:
    """Verifica saúde de serviços externos."""
    
    services = []
    
    # MediaMTX
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get("http://mediamtx:9997/v3/config/global/get")
            services.append(SystemHealth(
                service="MediaMTX",
                status="healthy" if response.status_code == 200 else "degraded",
                message="Streaming server operational"
            ))
    except:
        services.append(SystemHealth(
            service="MediaMTX",
            status="unhealthy",
            message="Cannot connect to streaming server"
        ))
    
    # RabbitMQ
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(
                "http://rabbitmq:15672/api/healthchecks/node",
                auth=("gtvision", "gtvision_password")
            )
            services.append(SystemHealth(
                service="RabbitMQ",
                status="healthy" if response.status_code == 200 else "degraded",
                message="Message broker operational"
            ))
    except:
        services.append(SystemHealth(
            service="RabbitMQ",
            status="unhealthy",
            message="Cannot connect to message broker"
        ))
    
    # MinIO
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get("http://minio:9000/minio/health/live")
            services.append(SystemHealth(
                service="MinIO",
                status="healthy" if response.status_code == 200 else "degraded",
                message="Storage operational"
            ))
    except:
        services.append(SystemHealth(
            service="MinIO",
            status="unhealthy",
            message="Cannot connect to storage"
        ))
    
    return services
