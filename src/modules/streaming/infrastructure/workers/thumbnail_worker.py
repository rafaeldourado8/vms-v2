import asyncio
import subprocess
from celery import Celery
from datetime import datetime
import boto3
from io import BytesIO


# Celery app
celery_app = Celery(
    'thumbnail_worker',
    broker='amqp://gtvision:gtvision_password@rabbitmq:5672/',
    backend='redis://redis:6379/0'
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


# MinIO client
s3_client = boto3.client(
    's3',
    endpoint_url='http://minio:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin'
)

BUCKET_NAME = 'gtvision-thumbnails'


@celery_app.task(name='generate_thumbnail')
def generate_thumbnail(camera_id: str, rtsp_url: str, tenant_id: str):
    """
    Gera thumbnail de câmera e armazena no MinIO.
    
    Executado periodicamente (a cada 10s) via Celery Beat.
    """
    try:
        # Capturar frame com FFmpeg
        cmd = [
            'ffmpeg',
            '-rtsp_transport', 'tcp',
            '-i', rtsp_url,
            '-frames:v', '1',
            '-vf', 'scale=320:-1',  # Thumbnail pequeno
            '-f', 'image2pipe',
            '-vcodec', 'mjpeg',
            '-q:v', '5',
            '-'
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=10
        )
        
        if result.returncode != 0:
            raise Exception(f"FFmpeg error: {result.stderr.decode()}")
        
        # Upload para MinIO
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        object_key = f"{tenant_id}/{camera_id}/thumbnails/{timestamp}.jpg"
        
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=object_key,
            Body=result.stdout,
            ContentType='image/jpeg',
            Metadata={
                'camera_id': camera_id,
                'tenant_id': tenant_id,
                'timestamp': timestamp
            }
        )
        
        # Manter apenas últimos 100 thumbnails (cleanup)
        cleanup_old_thumbnails(tenant_id, camera_id, keep_last=100)
        
        return {
            'status': 'success',
            'camera_id': camera_id,
            'object_key': object_key,
            'timestamp': timestamp
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'camera_id': camera_id,
            'error': str(e)
        }


def cleanup_old_thumbnails(tenant_id: str, camera_id: str, keep_last: int = 100):
    """Remove thumbnails antigos, mantendo apenas os últimos N."""
    try:
        prefix = f"{tenant_id}/{camera_id}/thumbnails/"
        
        # Listar objetos
        response = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=prefix
        )
        
        if 'Contents' not in response:
            return
        
        # Ordenar por data (mais recentes primeiro)
        objects = sorted(
            response['Contents'],
            key=lambda x: x['LastModified'],
            reverse=True
        )
        
        # Deletar excedentes
        to_delete = objects[keep_last:]
        if to_delete:
            delete_keys = [{'Key': obj['Key']} for obj in to_delete]
            s3_client.delete_objects(
                Bucket=BUCKET_NAME,
                Delete={'Objects': delete_keys}
            )
            
    except Exception as e:
        print(f"Cleanup error: {e}")


@celery_app.task(name='generate_timeline')
def generate_timeline(camera_id: str, start_time: str, end_time: str, tenant_id: str):
    """
    Gera timeline de thumbnails para um período.
    
    Usado para navegação rápida em gravações.
    """
    try:
        prefix = f"{tenant_id}/{camera_id}/thumbnails/"
        
        response = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=prefix
        )
        
        if 'Contents' not in response:
            return {'thumbnails': []}
        
        # Filtrar por período
        thumbnails = []
        for obj in response['Contents']:
            # TODO: Filtrar por start_time e end_time
            thumbnails.append({
                'url': f"http://minio:9000/{BUCKET_NAME}/{obj['Key']}",
                'timestamp': obj['LastModified'].isoformat(),
                'size': obj['Size']
            })
        
        return {
            'camera_id': camera_id,
            'thumbnails': thumbnails,
            'count': len(thumbnails)
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


# Celery Beat Schedule
celery_app.conf.beat_schedule = {
    'generate-thumbnails-every-10s': {
        'task': 'generate_thumbnail',
        'schedule': 10.0,
        # TODO: Buscar lista de câmeras ativas do banco
        'args': ('cam01', 'rtsp://...', 'tenant01')
    },
}
