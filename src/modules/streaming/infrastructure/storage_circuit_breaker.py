import shutil
from fastapi import HTTPException
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class StorageCircuitBreaker:
    """
    Circuit Breaker para proteção de disco.
    
    Bloqueia gravações quando storage > 95% para evitar crash.
    """
    
    def __init__(self, threshold_percent: float = 95.0):
        self.threshold_percent = threshold_percent
        self.is_open = False
        self.last_check = None
    
    def check_storage(self, path: str = "/") -> Dict:
        """
        Verifica uso de disco.
        
        Returns:
            dict: {
                "total_gb": float,
                "used_gb": float,
                "free_gb": float,
                "percent_used": float,
                "circuit_open": bool
            }
        """
        
        stat = shutil.disk_usage(path)
        
        total_gb = stat.total / (1024**3)
        used_gb = stat.used / (1024**3)
        free_gb = stat.free / (1024**3)
        percent_used = (stat.used / stat.total) * 100
        
        # Abrir circuit breaker se > threshold
        if percent_used >= self.threshold_percent:
            if not self.is_open:
                logger.critical(
                    f"CIRCUIT BREAKER OPENED: Disk usage {percent_used:.1f}% >= {self.threshold_percent}%"
                )
                self.is_open = True
        else:
            # Fechar circuit breaker se < threshold - 5%
            if self.is_open and percent_used < (self.threshold_percent - 5):
                logger.info(
                    f"CIRCUIT BREAKER CLOSED: Disk usage {percent_used:.1f}% < {self.threshold_percent - 5}%"
                )
                self.is_open = False
        
        return {
            "total_gb": round(total_gb, 2),
            "used_gb": round(used_gb, 2),
            "free_gb": round(free_gb, 2),
            "percent_used": round(percent_used, 2),
            "circuit_open": self.is_open,
            "threshold_percent": self.threshold_percent
        }
    
    def allow_recording(self) -> bool:
        """Verifica se gravação é permitida."""
        return not self.is_open
    
    def raise_if_open(self):
        """Lança exceção se circuit breaker estiver aberto."""
        if self.is_open:
            raise HTTPException(
                status_code=507,  # Insufficient Storage
                detail="Storage circuit breaker is open. Disk usage exceeded threshold."
            )


# Singleton
circuit_breaker = StorageCircuitBreaker(threshold_percent=95.0)


# Middleware para verificar antes de gravações
async def check_storage_middleware(request):
    """Middleware para verificar storage antes de operações de gravação."""
    
    # Verificar apenas em rotas de gravação
    if request.method == "POST" and "/recordings" in request.url.path:
        circuit_breaker.check_storage()
        circuit_breaker.raise_if_open()
    
    return request
