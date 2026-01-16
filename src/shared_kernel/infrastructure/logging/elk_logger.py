"""ELK Stack Logger"""
import json
import socket
import os
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID


class ELKLogger:
    """Logger for ELK Stack (Elasticsearch, Logstash, Kibana)"""
    
    def __init__(self, host: Optional[str] = None, port: int = 5000):
        self.host = host or os.getenv("LOGSTASH_HOST", "localhost")
        self.port = port
    
    def _send(self, data: Dict[str, Any]) -> None:
        """Send log to Logstash"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((self.host, self.port))
            message = json.dumps(data) + "\n"
            sock.sendall(message.encode('utf-8'))
            sock.close()
        except Exception:
            pass  # Silent fail
    
    def log_security_audit(
        self,
        action: str,
        user_id: UUID,
        ip_address: Optional[str] = None,
        resource: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log security audit event"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "audit_action": action,
            "user_id": str(user_id),
            "ip_address": ip_address,
            "resource": resource,
            "details": details or {},
            "service": "streaming"
        }
        self._send(log_data)
    
    def log_application(
        self,
        level: str,
        message: str,
        service: str = "streaming",
        **kwargs
    ) -> None:
        """Log application event"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            "service": service,
            **kwargs
        }
        self._send(log_data)


elk_logger = ELKLogger()
