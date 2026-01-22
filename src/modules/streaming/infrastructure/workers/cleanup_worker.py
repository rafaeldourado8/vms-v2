from celery import Celery
from datetime import datetime, timedelta
import boto3
from sqlalchemy import create_engine, text
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

celery_app = Celery(
    'cleanup_worker',
    broker='amqp://gtvision:gtvision_password@rabbitmq:5672/',
    backend='redis://redis:6379/0'
)

# MinIO
s3_client = boto3.client(
    's3',
    endpoint_url='http://minio:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin'
)

# PostgreSQL
engine = create_engine('postgresql://gtvision:gtvision_password@postgres:5432/gtvision')


@celery_app.task(name='cleanup_recordings')
def cleanup_recordings():
    """
    Worker de expurgo inteligente que respeita flags LGPD.
    
    Regras:
    - Respeita retention_days do plano do tenant
    - NÃO deleta gravações com flag incident=true
    - NÃO deleta gravações com flag legal_hold=true
    - Registra todas as exclusões em audit_log
    """
    
    with engine.connect() as conn:
        # Buscar gravações elegíveis para exclusão
        query = text("""
            SELECT 
                r.id,
                r.tenant_id,
                r.camera_id,
                r.start_time,
                r.end_time,
                r.storage_path,
                r.size_bytes,
                p.retention_days
            FROM recordings r
            JOIN cameras c ON r.camera_id = c.id
            JOIN cidades ci ON c.tenant_id = ci.id
            JOIN planos p ON ci.plano_id = p.id
            WHERE 
                r.incident = false
                AND r.legal_hold = false
                AND r.start_time < NOW() - (p.retention_days || ' days')::INTERVAL
                AND r.deleted_at IS NULL
            ORDER BY r.start_time ASC
            LIMIT 1000
        """)
        
        recordings = conn.execute(query).fetchall()
        
        deleted_count = 0
        freed_bytes = 0
        
        for rec in recordings:
            try:
                # Deletar do MinIO
                bucket = f"gtvision-recordings-{rec.tenant_id}"
                s3_client.delete_object(Bucket=bucket, Key=rec.storage_path)
                
                # Marcar como deletado no banco
                update_query = text("""
                    UPDATE recordings 
                    SET deleted_at = NOW(), deleted_by = 'cleanup_worker'
                    WHERE id = :id
                """)
                conn.execute(update_query, {"id": rec.id})
                
                # Registrar auditoria
                audit_query = text("""
                    INSERT INTO audit_logs (
                        tenant_id, action, resource_type, resource_id, 
                        metadata, created_at
                    ) VALUES (
                        :tenant_id, 'recording.deleted', 'recording', :recording_id,
                        :metadata, NOW()
                    )
                """)
                conn.execute(audit_query, {
                    "tenant_id": rec.tenant_id,
                    "recording_id": rec.id,
                    "metadata": {
                        "reason": "retention_policy",
                        "retention_days": rec.retention_days,
                        "size_bytes": rec.size_bytes,
                        "camera_id": rec.camera_id,
                        "start_time": rec.start_time.isoformat()
                    }
                })
                
                deleted_count += 1
                freed_bytes += rec.size_bytes
                
            except Exception as e:
                logger.error(f"Failed to delete recording {rec.id}: {e}")
                continue
        
        conn.commit()
        
        return {
            "status": "success",
            "deleted_count": deleted_count,
            "freed_bytes": freed_bytes,
            "freed_gb": round(freed_bytes / (1024**3), 2)
        }


@celery_app.task(name='anonymize_old_detections')
def anonymize_old_detections():
    """
    Anonimiza detecções antigas conforme LGPD.
    
    Remove dados sensíveis (placas, imagens) mas mantém estatísticas.
    """
    
    with engine.connect() as conn:
        # Anonimizar detecções > 90 dias (exceto incidentes)
        query = text("""
            UPDATE deteccoes
            SET 
                dados = jsonb_set(
                    dados,
                    '{placa}',
                    '"***ANONIMIZADO***"'
                ),
                imagem_url = NULL,
                anonymized_at = NOW()
            WHERE 
                timestamp < NOW() - INTERVAL '90 days'
                AND incident = false
                AND anonymized_at IS NULL
            RETURNING id, tenant_id
        """)
        
        result = conn.execute(query)
        anonymized = result.fetchall()
        
        # Registrar auditoria
        for det in anonymized:
            audit_query = text("""
                INSERT INTO audit_logs (
                    tenant_id, action, resource_type, resource_id, created_at
                ) VALUES (
                    :tenant_id, 'detection.anonymized', 'detection', :detection_id, NOW()
                )
            """)
            conn.execute(audit_query, {
                "tenant_id": det.tenant_id,
                "detection_id": det.id
            })
        
        conn.commit()
        
        return {
            "status": "success",
            "anonymized_count": len(anonymized)
        }


# Celery Beat Schedule
celery_app.conf.beat_schedule = {
    'cleanup-recordings-daily': {
        'task': 'cleanup_recordings',
        'schedule': 86400.0,  # 24h
    },
    'anonymize-detections-daily': {
        'task': 'anonymize_old_detections',
        'schedule': 86400.0,  # 24h
    },
}
