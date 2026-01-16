"""Audit Log Module"""
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class AuditAction(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    DATA_ACCESS = "data_access"
    DATA_EXPORT = "data_export"
    DATA_DELETE = "data_delete"
    CONSENT_REVOKED = "consent_revoked"
    STREAM_START = "stream_start"
    STREAM_STOP = "stream_stop"
    RECORDING_START = "recording_start"
    RECORDING_STOP = "recording_stop"


class AuditLog:
    """In-memory audit log (substituir por banco em produção)"""
    _logs = []
    
    @classmethod
    def record(
        cls,
        action: AuditAction,
        user_id: Optional[UUID] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[UUID] = None,
        ip_address: Optional[str] = None,
        details: Optional[dict] = None
    ):
        """Registra log de auditoria"""
        log = {
            "id": uuid4(),
            "timestamp": datetime.now(),
            "action": action.value,
            "user_id": str(user_id) if user_id else None,
            "resource_type": resource_type,
            "resource_id": str(resource_id) if resource_id else None,
            "ip_address": ip_address,
            "details": details or {}
        }
        cls._logs.append(log)
        return log
    
    @classmethod
    def get_user_logs(cls, user_id: UUID, limit: int = 100):
        """Obtém logs de um usuário"""
        return [
            log for log in cls._logs
            if log["user_id"] == str(user_id)
        ][:limit]
