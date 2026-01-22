import asyncio
import socket
from typing import Optional
from datetime import datetime
from urllib.parse import urlparse


class CameraHealthService:
    """Serviço para verificar conectividade de câmeras RTSP."""
    
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
    
    async def check_rtsp_connectivity(self, rtsp_url: str) -> dict:
        """
        Testa conectividade RTSP básica (TCP handshake).
        
        Returns:
            dict: {
                "online": bool,
                "latency_ms": float,
                "error": Optional[str],
                "checked_at": str
            }
        """
        start_time = datetime.utcnow()
        
        try:
            parsed = urlparse(rtsp_url)
            host = parsed.hostname
            port = parsed.port or 554
            
            if not host:
                return {
                    "online": False,
                    "latency_ms": 0,
                    "error": "Invalid RTSP URL",
                    "checked_at": start_time.isoformat()
                }
            
            # Tenta conexão TCP
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=self.timeout
            )
            
            writer.close()
            await writer.wait_closed()
            
            end_time = datetime.utcnow()
            latency_ms = (end_time - start_time).total_seconds() * 1000
            
            return {
                "online": True,
                "latency_ms": round(latency_ms, 2),
                "error": None,
                "checked_at": start_time.isoformat()
            }
            
        except asyncio.TimeoutError:
            return {
                "online": False,
                "latency_ms": 0,
                "error": f"Timeout after {self.timeout}s",
                "checked_at": start_time.isoformat()
            }
        except socket.gaierror:
            return {
                "online": False,
                "latency_ms": 0,
                "error": "DNS resolution failed",
                "checked_at": start_time.isoformat()
            }
        except ConnectionRefusedError:
            return {
                "online": False,
                "latency_ms": 0,
                "error": "Connection refused",
                "checked_at": start_time.isoformat()
            }
        except Exception as e:
            return {
                "online": False,
                "latency_ms": 0,
                "error": str(e),
                "checked_at": start_time.isoformat()
            }
    
    async def check_multiple_cameras(self, cameras: list[dict]) -> list[dict]:
        """
        Verifica múltiplas câmeras em paralelo.
        
        Args:
            cameras: Lista de dicts com {"id": str, "rtsp_url": str}
        
        Returns:
            Lista de resultados com camera_id incluído
        """
        tasks = []
        for camera in cameras:
            task = self._check_camera_with_id(camera["id"], camera["rtsp_url"])
            tasks.append(task)
        
        return await asyncio.gather(*tasks)
    
    async def _check_camera_with_id(self, camera_id: str, rtsp_url: str) -> dict:
        result = await self.check_rtsp_connectivity(rtsp_url)
        result["camera_id"] = camera_id
        return result
