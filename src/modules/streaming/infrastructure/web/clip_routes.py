import subprocess
import tempfile
import os
from fastapi import APIRouter, HTTPException, Header, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import boto3
from uuid import uuid4

router = APIRouter(prefix="/clips", tags=["clips"])

s3_client = boto3.client(
    's3',
    endpoint_url='http://minio:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin'
)


class CreateClipRequest(BaseModel):
    camera_id: str
    start_time: datetime
    end_time: datetime
    reason: str  # "evidence", "incident", "export"
    incident_flag: bool = False


class ClipResponse(BaseModel):
    id: str
    status: str
    download_url: Optional[str] = None


class ClipExportService:
    """Serviço para exportação de clipes MP4 com stitching."""
    
    async def export_clip(
        self,
        tenant_id: str,
        camera_id: str,
        start_time: datetime,
        end_time: datetime,
        clip_id: str
    ) -> dict:
        """
        Exporta clipe MP4 fazendo stitching de segmentos HLS.
        
        Processo:
        1. Busca segmentos .ts do período no MinIO
        2. Concatena com FFmpeg
        3. Gera MP4 final
        4. Upload para MinIO
        """
        
        try:
            # Buscar segmentos do período
            segments = await self._list_segments(tenant_id, camera_id, start_time, end_time)
            
            if not segments:
                raise Exception("No segments found for the specified period")
            
            # Criar arquivo temporário para lista de segmentos
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                segment_list_path = f.name
                for seg in segments:
                    # Download segment
                    local_path = f"/tmp/{seg['key'].split('/')[-1]}"
                    s3_client.download_file(
                        Bucket=seg['bucket'],
                        Key=seg['key'],
                        Filename=local_path
                    )
                    f.write(f"file '{local_path}'\n")
            
            # Concatenar com FFmpeg
            output_path = f"/tmp/{clip_id}.mp4"
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', segment_list_path,
                '-c', 'copy',
                '-movflags', '+faststart',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=300)
            
            if result.returncode != 0:
                raise Exception(f"FFmpeg error: {result.stderr.decode()}")
            
            # Upload MP4 para MinIO
            bucket = f"gtvision-clips-{tenant_id}"
            key = f"{camera_id}/clips/{clip_id}.mp4"
            
            with open(output_path, 'rb') as f:
                s3_client.put_object(
                    Bucket=bucket,
                    Key=key,
                    Body=f,
                    ContentType='video/mp4',
                    Metadata={
                        'camera_id': camera_id,
                        'start_time': start_time.isoformat(),
                        'end_time': end_time.isoformat(),
                        'clip_id': clip_id
                    }
                )
            
            # Cleanup
            os.unlink(segment_list_path)
            os.unlink(output_path)
            for seg in segments:
                local_path = f"/tmp/{seg['key'].split('/')[-1]}"
                if os.path.exists(local_path):
                    os.unlink(local_path)
            
            # Gerar URL de download (válida por 7 dias)
            download_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': key},
                ExpiresIn=604800  # 7 dias
            )
            
            return {
                "status": "completed",
                "download_url": download_url,
                "size_bytes": os.path.getsize(output_path)
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    async def _list_segments(
        self,
        tenant_id: str,
        camera_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> list:
        """Lista segmentos HLS do período."""
        
        bucket = f"gtvision-recordings-{tenant_id}"
        prefix = f"{camera_id}/segments/"
        
        # TODO: Filtrar por timestamp dos segmentos
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        
        segments = []
        if 'Contents' in response:
            for obj in response['Contents']:
                # Filtrar por período (simplificado)
                segments.append({
                    'bucket': bucket,
                    'key': obj['Key'],
                    'size': obj['Size']
                })
        
        return segments


clip_service = ClipExportService()


@router.post("", response_model=ClipResponse, status_code=202)
async def create_clip(
    request: CreateClipRequest,
    background_tasks: BackgroundTasks,
    x_tenant_id: str = Header(...)
):
    """
    Cria clipe MP4 para evidência/exportação.
    
    Processo assíncrono:
    1. Retorna 202 Accepted imediatamente
    2. Processa em background
    3. Cliente consulta status via GET /clips/{id}
    """
    
    clip_id = str(uuid4())
    
    # Processar em background
    background_tasks.add_task(
        clip_service.export_clip,
        x_tenant_id,
        request.camera_id,
        request.start_time,
        request.end_time,
        clip_id
    )
    
    # TODO: Salvar no banco com status "processing"
    
    return ClipResponse(
        id=clip_id,
        status="processing"
    )


@router.get("/{clip_id}", response_model=ClipResponse)
async def get_clip_status(
    clip_id: str,
    x_tenant_id: str = Header(...)
):
    """Consulta status de exportação do clipe."""
    
    # TODO: Buscar do banco
    return ClipResponse(
        id=clip_id,
        status="completed",
        download_url="https://minio:9000/..."
    )
