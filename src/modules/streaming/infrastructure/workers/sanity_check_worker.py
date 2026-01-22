from celery import Celery
import boto3
from sqlalchemy import create_engine, text
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

celery_app = Celery(
    'sanity_check_worker',
    broker='amqp://gtvision:gtvision_password@rabbitmq:5672/',
    backend='redis://redis:6379/0'
)

s3_client = boto3.client(
    's3',
    endpoint_url='http://minio:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin'
)

engine = create_engine('postgresql://gtvision:gtvision_password@postgres:5432/gtvision')


@celery_app.task(name='sanity_check_storage')
def sanity_check_storage():
    """
    Job noturno de integridade: detecta arquivos órfãos.
    
    Verifica:
    1. Arquivos no MinIO sem registro no banco (órfãos)
    2. Registros no banco sem arquivo no MinIO (inconsistência)
    3. Tamanho reportado vs tamanho real
    """
    
    results = {
        "orphaned_files": [],
        "missing_files": [],
        "size_mismatches": [],
        "total_checked": 0
    }
    
    with engine.connect() as conn:
        # Buscar todos os tenants
        tenants_query = text("SELECT id FROM cidades")
        tenants = conn.execute(tenants_query).fetchall()
        
        for tenant in tenants:
            tenant_id = tenant.id
            bucket = f"gtvision-recordings-{tenant_id}"
            
            try:
                # 1. Listar arquivos no MinIO
                response = s3_client.list_objects_v2(Bucket=bucket)
                
                if 'Contents' not in response:
                    continue
                
                minio_files = {obj['Key']: obj['Size'] for obj in response['Contents']}
                
                # 2. Buscar registros no banco
                db_query = text("""
                    SELECT storage_path, size_bytes, id
                    FROM recordings
                    WHERE tenant_id = :tenant_id AND deleted_at IS NULL
                """)
                db_records = conn.execute(db_query, {"tenant_id": tenant_id}).fetchall()
                
                db_paths = {rec.storage_path: (rec.size_bytes, rec.id) for rec in db_records}
                
                # 3. Detectar órfãos (no MinIO mas não no banco)
                for path, size in minio_files.items():
                    results["total_checked"] += 1
                    
                    if path not in db_paths:
                        results["orphaned_files"].append({
                            "tenant_id": tenant_id,
                            "path": path,
                            "size_bytes": size
                        })
                        logger.warning(f"Orphaned file detected: {path}")
                
                # 4. Detectar arquivos faltando (no banco mas não no MinIO)
                for path, (size, rec_id) in db_paths.items():
                    if path not in minio_files:
                        results["missing_files"].append({
                            "tenant_id": tenant_id,
                            "recording_id": rec_id,
                            "path": path
                        })
                        logger.error(f"Missing file: {path}")
                    
                    # 5. Verificar tamanho
                    elif abs(minio_files[path] - size) > 1024:  # Tolerância de 1KB
                        results["size_mismatches"].append({
                            "tenant_id": tenant_id,
                            "recording_id": rec_id,
                            "path": path,
                            "db_size": size,
                            "minio_size": minio_files[path]
                        })
                        logger.warning(f"Size mismatch: {path}")
                
            except Exception as e:
                logger.error(f"Sanity check failed for tenant {tenant_id}: {e}")
                continue
        
        # Registrar resultado em audit_log
        audit_query = text("""
            INSERT INTO audit_logs (
                tenant_id, action, resource_type, metadata, created_at
            ) VALUES (
                'system', 'sanity_check.completed', 'storage', :metadata, NOW()
            )
        """)
        conn.execute(audit_query, {"metadata": results})
        conn.commit()
    
    # Enviar alerta se houver problemas críticos
    if results["missing_files"] or len(results["orphaned_files"]) > 100:
        logger.critical(f"SANITY CHECK ALERT: {results}")
        # TODO: Enviar notificação para admin
    
    return results


@celery_app.task(name='cleanup_orphaned_files')
def cleanup_orphaned_files(dry_run: bool = True):
    """
    Remove arquivos órfãos detectados pelo sanity check.
    
    Args:
        dry_run: Se True, apenas lista sem deletar
    """
    
    # Executar sanity check primeiro
    check_result = sanity_check_storage()
    
    deleted_count = 0
    freed_bytes = 0
    
    for orphan in check_result["orphaned_files"]:
        try:
            if not dry_run:
                bucket = f"gtvision-recordings-{orphan['tenant_id']}"
                s3_client.delete_object(Bucket=bucket, Key=orphan['path'])
                deleted_count += 1
                freed_bytes += orphan['size_bytes']
                logger.info(f"Deleted orphaned file: {orphan['path']}")
            else:
                logger.info(f"[DRY RUN] Would delete: {orphan['path']}")
        
        except Exception as e:
            logger.error(f"Failed to delete orphan {orphan['path']}: {e}")
    
    return {
        "dry_run": dry_run,
        "deleted_count": deleted_count,
        "freed_bytes": freed_bytes,
        "freed_gb": round(freed_bytes / (1024**3), 2)
    }


# Celery Beat Schedule
celery_app.conf.beat_schedule = {
    'sanity-check-nightly': {
        'task': 'sanity_check_storage',
        'schedule': 86400.0,  # 24h
        'options': {'expires': 3600}  # Expira em 1h se não executar
    },
}
