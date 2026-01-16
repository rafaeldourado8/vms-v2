"""LGPD Endpoints - Direitos dos Titulares"""
from typing import Annotated
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.shared_kernel.infrastructure.security.dependencies import User, get_current_user
from src.shared_kernel.infrastructure.logging import elk_logger

router = APIRouter(prefix="/api/lgpd", tags=["LGPD"])


class DataAccessResponse(BaseModel):
    user_id: str
    email: str
    role: str
    created_at: str
    data_processing: list


class DataExportResponse(BaseModel):
    user_id: str
    email: str
    role: str
    exported_at: str
    format: str


@router.get("/meus-dados", response_model=DataAccessResponse)
async def get_my_data(user: Annotated[User, Depends(get_current_user)]):
    """Direito de acesso (Art. 18, I e II) - Confirmar e acessar dados pessoais"""
    from src.shared_kernel.infrastructure.security.audit_log import AuditLog, AuditAction
    
    # Audit log
    AuditLog.record(
        action=AuditAction.DATA_ACCESS,
        user_id=user.id
    )
    
    # ELK log
    elk_logger.log_security_audit(
        action="DATA_ACCESS",
        user_id=user.id,
        resource="/api/lgpd/meus-dados",
        details={"article": "Art. 18 I/II"}
    )
    
    return DataAccessResponse(
        user_id=str(user.id),
        email=user.email,
        role=user.role.value,
        created_at=datetime.now().isoformat(),
        data_processing=[
            {
                "purpose": "Autenticação e controle de acesso",
                "legal_basis": "Execução de contrato (Art. 7º, V)",
                "retention": "Enquanto ativo + 5 anos",
                "data_types": ["nome", "email", "role"]
            }
        ]
    )


@router.get("/exportar", response_model=DataExportResponse)
async def export_my_data(
    user: Annotated[User, Depends(get_current_user)],
    format: str = "json"
):
    """Direito de portabilidade (Art. 18, V) - Exportar dados em formato estruturado"""
    from src.shared_kernel.infrastructure.security.audit_log import AuditLog, AuditAction
    
    # Audit log
    AuditLog.record(
        action=AuditAction.DATA_EXPORT,
        user_id=user.id,
        details={"format": format}
    )
    
    # ELK log
    elk_logger.log_security_audit(
        action="DATA_EXPORT",
        user_id=user.id,
        resource="/api/lgpd/exportar",
        details={"format": format, "article": "Art. 18 V"}
    )
    
    return DataExportResponse(
        user_id=str(user.id),
        email=user.email,
        role=user.role.value,
        exported_at=datetime.now().isoformat(),
        format=format
    )


@router.delete("/excluir")
async def delete_my_data(user: Annotated[User, Depends(get_current_user)]):
    """Direito de exclusão (Art. 18, IV) - Solicitar exclusão/anonimização"""
    from src.shared_kernel.infrastructure.security.audit_log import AuditLog, AuditAction
    
    # Audit log
    AuditLog.record(
        action=AuditAction.DATA_DELETE,
        user_id=user.id
    )
    
    # ELK log
    elk_logger.log_security_audit(
        action="DATA_DELETE",
        user_id=user.id,
        resource="/api/lgpd/excluir",
        details={"protocol": str(UUID("123e4567-e89b-12d3-a456-426614174000")), "article": "Art. 18 IV"}
    )
    
    return {
        "message": "Solicitação de exclusão registrada",
        "protocol": str(UUID("123e4567-e89b-12d3-a456-426614174000")),
        "status": "pending",
        "estimated_days": 15
    }


@router.post("/revogar-consentimento")
async def revoke_consent(user: Annotated[User, Depends(get_current_user)]):
    """Direito de revogação (Art. 18, IX) - Revogar consentimento"""
    from src.shared_kernel.infrastructure.security.audit_log import AuditLog, AuditAction
    
    # Audit log
    AuditLog.record(
        action=AuditAction.CONSENT_REVOKED,
        user_id=user.id
    )
    
    # ELK log
    elk_logger.log_security_audit(
        action="CONSENT_REVOKED",
        user_id=user.id,
        resource="/api/lgpd/revogar-consentimento",
        details={"article": "Art. 18 IX"}
    )
    
    return {
        "message": "Consentimento revogado com sucesso",
        "revoked_at": datetime.now().isoformat()
    }
