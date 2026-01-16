# 9️⃣ Auditoria e Logs

Sistema de logs e rastreabilidade para compliance LGPD (Art. 37 e 46).

## 📋 Requisitos de Auditoria

### Princípio da Accountability (Art. 6º, X)
Demonstrar medidas eficazes e capazes de comprovar cumprimento da LGPD.

### Registro de Operações (Art. 37)
Controlador e operador devem manter registro das operações de tratamento.

## 🎯 O Que Auditar

### 1. Acesso a Dados Pessoais
- Login/logout
- Consulta de dados
- Exportação de dados
- Visualização de relatórios

### 2. Modificação de Dados
- Criação de usuário
- Atualização de dados
- Exclusão/anonimização
- Correção de dados

### 3. Consentimento
- Concessão de consentimento
- Revogação de consentimento
- Renovação de consentimento

### 4. Direitos dos Titulares
- Solicitação de acesso
- Solicitação de correção
- Solicitação de exclusão
- Solicitação de portabilidade
- Oposição ao tratamento

### 5. Segurança
- Tentativas de login falhadas
- Alteração de permissões
- Alteração de configurações
- Incidentes de segurança

### 6. Compartilhamento
- Compartilhamento com terceiros
- Transferência internacional
- Acesso por fornecedores

## 💻 Implementação

### Modelo de Log de Auditoria

```python
from enum import Enum
from datetime import datetime
from uuid import UUID
from typing import Optional, Dict

class AuditAction(str, Enum):
    # Autenticação
    LOGIN = "login"
    LOGOUT = "logout"
    LOGIN_FAILED = "login_failed"
    
    # Acesso a dados
    DATA_ACCESS = "data_access"
    DATA_EXPORT = "data_export"
    DATA_VIEW = "data_view"
    
    # Modificação de dados
    DATA_CREATE = "data_create"
    DATA_UPDATE = "data_update"
    DATA_DELETE = "data_delete"
    DATA_ANONYMIZE = "data_anonymize"
    
    # Consentimento
    CONSENT_GRANTED = "consent_granted"
    CONSENT_REVOKED = "consent_revoked"
    
    # Direitos dos titulares
    RIGHT_ACCESS = "right_access"
    RIGHT_CORRECTION = "right_correction"
    RIGHT_DELETION = "right_deletion"
    RIGHT_PORTABILITY = "right_portability"
    
    # Segurança
    PERMISSION_CHANGED = "permission_changed"
    CONFIG_CHANGED = "config_changed"
    INCIDENT_REPORTED = "incident_reported"

class AuditLog:
    id: UUID
    timestamp: datetime
    user_id: Optional[UUID]  # None para ações do sistema
    action: AuditAction
    resource_type: str  # "User", "Stream", "Recording"
    resource_id: Optional[UUID]
    ip_address: str
    user_agent: str
    details: Dict  # JSON com detalhes específicos
    success: bool
    error_message: Optional[str]
```

### Serviço de Auditoria

```python
class AuditService:
    @staticmethod
    def log(
        action: AuditAction,
        user_id: Optional[UUID] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[UUID] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[Dict] = None,
        success: bool = True,
        error_message: Optional[str] = None
    ):
        """Registra log de auditoria"""
        
        log = AuditLog.create(
            timestamp=datetime.now(),
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details or {},
            success=success,
            error_message=error_message
        )
        
        # Log também no sistema de logging
        logger.info(
            f"AUDIT: {action} by user {user_id} on {resource_type}:{resource_id}",
            extra={
                "audit_log_id": log.id,
                "user_id": user_id,
                "action": action,
                "success": success
            }
        )
        
        return log
```

### Decorator de Auditoria

```python
from functools import wraps
from fastapi import Request

def audit_log(action: AuditAction, resource_type: str):
    """Decorator para auditar endpoints"""
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extrair request e user
            request: Request = kwargs.get("request")
            user: User = kwargs.get("user") or kwargs.get("current_user")
            
            # Executar função
            try:
                result = await func(*args, **kwargs)
                
                # Log de sucesso
                AuditService.log(
                    action=action,
                    user_id=user.id if user else None,
                    resource_type=resource_type,
                    resource_id=result.get("id") if isinstance(result, dict) else None,
                    ip_address=request.client.host if request else None,
                    user_agent=request.headers.get("user-agent") if request else None,
                    success=True
                )
                
                return result
                
            except Exception as e:
                # Log de erro
                AuditService.log(
                    action=action,
                    user_id=user.id if user else None,
                    resource_type=resource_type,
                    ip_address=request.client.host if request else None,
                    user_agent=request.headers.get("user-agent") if request else None,
                    success=False,
                    error_message=str(e)
                )
                raise
        
        return wrapper
    return decorator
```

### Uso do Decorator

```python
@router.get("/api/users/{user_id}")
@audit_log(action=AuditAction.DATA_ACCESS, resource_type="User")
async def get_user(
    user_id: UUID,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Consulta usuário (auditado automaticamente)"""
    user = User.get(user_id)
    return user.to_dict()

@router.post("/api/users")
@audit_log(action=AuditAction.DATA_CREATE, resource_type="User")
async def create_user(
    request: Request,
    data: CreateUserDTO,
    current_user: User = Depends(require_admin)
):
    """Cria usuário (auditado automaticamente)"""
    user = User.create(**data.dict())
    return {"id": user.id}

@router.delete("/api/users/{user_id}")
@audit_log(action=AuditAction.DATA_DELETE, resource_type="User")
async def delete_user(
    user_id: UUID,
    request: Request,
    current_user: User = Depends(require_admin)
):
    """Exclui usuário (auditado automaticamente)"""
    user = User.get(user_id)
    user.delete()
    return {"message": "Usuário excluído"}
```

### Auditoria Manual

```python
# Login
@router.post("/api/auth/login")
async def login(request: Request, credentials: LoginDTO):
    user = authenticate(credentials.email, credentials.password)
    
    if user:
        # Login bem-sucedido
        AuditService.log(
            action=AuditAction.LOGIN,
            user_id=user.id,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            success=True
        )
        return {"token": create_token(user)}
    else:
        # Login falhado
        AuditService.log(
            action=AuditAction.LOGIN_FAILED,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent"),
            details={"email": credentials.email},
            success=False,
            error_message="Credenciais inválidas"
        )
        raise HTTPException(401, "Credenciais inválidas")

# Consentimento
@router.post("/api/lgpd/consentimento/conceder")
async def grant_consent(
    request: Request,
    data: GrantConsentDTO,
    user: User = Depends(get_current_user)
):
    consent = Consent.create(user_id=user.id, purpose=data.purpose)
    
    AuditService.log(
        action=AuditAction.CONSENT_GRANTED,
        user_id=user.id,
        resource_type="Consent",
        resource_id=consent.id,
        ip_address=request.client.host,
        details={"purpose": data.purpose}
    )
    
    return {"consent_id": consent.id}
```

## 📊 Consulta de Logs

### Endpoint de Auditoria

```python
@router.get("/api/audit-logs")
async def get_audit_logs(
    user_id: Optional[UUID] = None,
    action: Optional[AuditAction] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    page: int = 1,
    page_size: int = 50,
    admin: User = Depends(require_admin)
):
    """Consulta logs de auditoria (apenas admin)"""
    
    query = AuditLog.query()
    
    if user_id:
        query = query.filter(user_id=user_id)
    
    if action:
        query = query.filter(action=action)
    
    if start_date:
        query = query.filter(timestamp__gte=start_date)
    
    if end_date:
        query = query.filter(timestamp__lte=end_date)
    
    total = query.count()
    logs = query.order_by("-timestamp").paginate(page, page_size)
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "logs": [log.to_dict() for log in logs]
    }

@router.get("/api/audit-logs/user/{user_id}")
async def get_user_audit_trail(
    user_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """Histórico de auditoria do usuário"""
    
    # Usuário pode ver apenas seus próprios logs
    if current_user.id != user_id and current_user.role != Role.ADMIN:
        raise HTTPException(403, "Não autorizado")
    
    logs = AuditLog.filter(user_id=user_id).order_by("-timestamp").limit(100)
    
    return {
        "user_id": user_id,
        "logs": [
            {
                "timestamp": log.timestamp,
                "action": log.action,
                "resource": f"{log.resource_type}:{log.resource_id}",
                "success": log.success
            }
            for log in logs
        ]
    }
```

### Dashboard de Auditoria

```python
@router.get("/api/audit-logs/dashboard")
async def audit_dashboard(admin: User = Depends(require_admin)):
    """Dashboard de auditoria"""
    
    # Últimas 24 horas
    last_24h = datetime.now() - timedelta(hours=24)
    
    total_actions = AuditLog.filter(timestamp__gte=last_24h).count()
    failed_actions = AuditLog.filter(
        timestamp__gte=last_24h,
        success=False
    ).count()
    
    by_action = AuditLog.filter(
        timestamp__gte=last_24h
    ).group_by("action")
    
    by_user = AuditLog.filter(
        timestamp__gte=last_24h
    ).group_by("user_id").order_by("-count").limit(10)
    
    failed_logins = AuditLog.filter(
        timestamp__gte=last_24h,
        action=AuditAction.LOGIN_FAILED
    ).count()
    
    return {
        "period": "last_24h",
        "total_actions": total_actions,
        "failed_actions": failed_actions,
        "failure_rate": failed_actions / total_actions if total_actions > 0 else 0,
        "by_action": by_action,
        "top_users": by_user,
        "failed_logins": failed_logins
    }
```

## 🔍 Análise de Logs

### Detecção de Anomalias

```python
@celery.task
def analyze_audit_logs():
    """Analisa logs para detectar anomalias"""
    
    # 1. Múltiplos acessos fora do horário
    after_hours = AuditLog.filter(
        timestamp__hour__in=[22, 23, 0, 1, 2, 3, 4, 5],
        action=AuditAction.DATA_ACCESS
    ).group_by("user_id")
    
    for user_id, count in after_hours.items():
        if count >= 5:
            alert_security_team(
                f"Usuário {user_id} acessou dados {count} vezes fora do horário"
            )
    
    # 2. Múltiplas tentativas de login falhadas
    failed_logins = AuditLog.filter(
        timestamp__gte=datetime.now() - timedelta(minutes=10),
        action=AuditAction.LOGIN_FAILED
    ).group_by("ip_address")
    
    for ip, count in failed_logins.items():
        if count >= 5:
            block_ip(ip)
            alert_security_team(f"IP {ip} bloqueado após {count} tentativas")
    
    # 3. Exportação massiva de dados
    exports = AuditLog.filter(
        timestamp__gte=datetime.now() - timedelta(hours=1),
        action=AuditAction.DATA_EXPORT
    ).group_by("user_id")
    
    for user_id, count in exports.items():
        if count >= 10:
            alert_security_team(
                f"Usuário {user_id} exportou dados {count} vezes em 1 hora"
            )
```

## 📦 Retenção de Logs

### Política de Retenção

```python
class LogRetentionPolicy:
    # Logs de acesso: 6 meses
    ACCESS_LOGS = timedelta(days=180)
    
    # Logs de modificação: 1 ano
    MODIFICATION_LOGS = timedelta(days=365)
    
    # Logs de incidentes: 5 anos
    INCIDENT_LOGS = timedelta(days=1825)
    
    # Logs de consentimento: Enquanto houver relação + 5 anos
    CONSENT_LOGS = None  # Não expira automaticamente

@celery.task
def cleanup_old_logs():
    """Remove logs antigos conforme política de retenção"""
    
    now = datetime.now()
    
    # Logs de acesso
    AuditLog.filter(
        action__in=[AuditAction.DATA_ACCESS, AuditAction.DATA_VIEW],
        timestamp__lt=now - LogRetentionPolicy.ACCESS_LOGS
    ).delete()
    
    # Logs de modificação
    AuditLog.filter(
        action__in=[
            AuditAction.DATA_CREATE,
            AuditAction.DATA_UPDATE,
            AuditAction.DATA_DELETE
        ],
        timestamp__lt=now - LogRetentionPolicy.MODIFICATION_LOGS
    ).delete()
    
    logger.info("Old audit logs cleaned up")
```

## 📄 Relatórios de Auditoria

### Relatório para ANPD

```python
@router.get("/api/audit-logs/report/anpd")
async def generate_anpd_report(
    start_date: datetime,
    end_date: datetime,
    admin: User = Depends(require_admin)
):
    """Gera relatório de auditoria para ANPD"""
    
    logs = AuditLog.filter(
        timestamp__gte=start_date,
        timestamp__lte=end_date
    )
    
    report = {
        "period": {
            "start": start_date,
            "end": end_date
        },
        "summary": {
            "total_operations": logs.count(),
            "by_action": logs.group_by("action"),
            "unique_users": logs.distinct("user_id").count(),
            "failed_operations": logs.filter(success=False).count()
        },
        "data_subject_rights": {
            "access_requests": logs.filter(action=AuditAction.RIGHT_ACCESS).count(),
            "correction_requests": logs.filter(action=AuditAction.RIGHT_CORRECTION).count(),
            "deletion_requests": logs.filter(action=AuditAction.RIGHT_DELETION).count(),
            "portability_requests": logs.filter(action=AuditAction.RIGHT_PORTABILITY).count()
        },
        "security_incidents": logs.filter(action=AuditAction.INCIDENT_REPORTED).count(),
        "consent_operations": {
            "granted": logs.filter(action=AuditAction.CONSENT_GRANTED).count(),
            "revoked": logs.filter(action=AuditAction.CONSENT_REVOKED).count()
        }
    }
    
    return report
```

## ✅ Checklist de Auditoria

- [ ] Modelo de log de auditoria implementado
- [ ] Serviço de auditoria criado
- [ ] Decorator de auditoria para endpoints
- [ ] Auditoria de login/logout
- [ ] Auditoria de acesso a dados
- [ ] Auditoria de modificação de dados
- [ ] Auditoria de consentimento
- [ ] Auditoria de direitos dos titulares
- [ ] Dashboard de auditoria
- [ ] Detecção de anomalias
- [ ] Política de retenção implementada
- [ ] Limpeza automática de logs antigos
- [ ] Relatórios para ANPD
- [ ] Logs protegidos contra alteração
