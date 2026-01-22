import asyncio
import subprocess
from fastapi import APIRouter, HTTPException, Header, Response
from fastapi.responses import StreamingResponse
import io


router = APIRouter(prefix="/snapshots", tags=["snapshots"])


class SnapshotService:
    """Serviço para captura de snapshots via FFmpeg."""
    
    async def capture_snapshot(self, rtsp_url: str, timeout: int = 10) -> bytes:
        """
        Captura snapshot de stream RTSP usando FFmpeg.
        
        Args:
            rtsp_url: URL RTSP da câmera
            timeout: Timeout em segundos
            
        Returns:
            bytes: Imagem JPEG
        """
        cmd = [
            "ffmpeg",
            "-rtsp_transport", "tcp",
            "-i", rtsp_url,
            "-frames:v", "1",
            "-f", "image2pipe",
            "-vcodec", "mjpeg",
            "-q:v", "2",
            "-"
        ]
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
            
            if process.returncode != 0:
                raise Exception(f"FFmpeg error: {stderr.decode()}")
            
            return stdout
            
        except asyncio.TimeoutError:
            if process:
                process.kill()
            raise Exception(f"Snapshot timeout after {timeout}s")
        except Exception as e:
            raise Exception(f"Failed to capture snapshot: {str(e)}")


snapshot_service = SnapshotService()


@router.get("/{camera_id}")
async def get_camera_snapshot(
    camera_id: str,
    x_tenant_id: str = Header(...)
):
    """
    Captura snapshot atual da câmera.
    
    Retorna imagem JPEG sem necessidade de carregar stream completo.
    """
    
    # TODO: Buscar rtsp_url do banco
    # Mock para exemplo
    rtsp_url = f"rtsp://admin:123@192.168.1.100:554/cam/realmonitor?channel=1&subtype=0"
    
    try:
        image_bytes = await snapshot_service.capture_snapshot(rtsp_url)
        
        return Response(
            content=image_bytes,
            media_type="image/jpeg",
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
