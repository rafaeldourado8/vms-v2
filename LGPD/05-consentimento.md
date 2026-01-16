# 5️⃣ Consentimento

Coleta e gestão de consentimento conforme LGPD (Art. 8º).

## 📋 Requisitos do Consentimento

### 1. Livre
- ❌ Não pode ser condição para serviço essencial
- ✅ Titular pode recusar sem prejuízo

### 2. Informado
- ✅ Finalidade específica
- ✅ Forma de tratamento
- ✅ Duração do tratamento
- ✅ Identificação do controlador
- ✅ Contato do DPO

### 3. Inequívoco
- ✅ Manifestação expressa (opt-in)
- ❌ Não pode ser tácito ou presumido
- ❌ Não pode ser pré-marcado

### 4. Específico
- ✅ Um consentimento por finalidade
- ❌ Não pode ser genérico

### 5. Destacado
- ✅ Separado de outros termos
- ✅ Linguagem clara e simples
- ✅ Fácil visualização

## 🎯 Quando Usar Consentimento

### ✅ Usar Consentimento
- Notificações por email/SMS
- Newsletter
- Compartilhamento com parceiros
- Uso de dados para marketing
- Cookies não essenciais

### ❌ Não Usar Consentimento
- Dados obrigatórios para contrato
- Obrigação legal
- Exercício regular de direito
- Segurança do sistema

## 💻 Implementação no GT-Vision

### Modelo de Dados

```python
from enum import Enum
from datetime import datetime
from uuid import UUID

class ConsentStatus(str, Enum):
    GRANTED = "granted"
    REVOKED = "revoked"
    EXPIRED = "expired"

class Consent:
    id: UUID
    user_id: UUID
    purpose: str  # Finalidade específica
    description: str  # Descrição clara
    granted_at: datetime
    revoked_at: Optional[datetime]
    expires_at: Optional[datetime]
    status: ConsentStatus
    ip_address: str  # Evidência
    user_agent: str  # Evidência
    version: int  # Versão do termo
```

### Endpoint de Consentimento

```python
from fastapi import APIRouter, Depends
from typing import List

router = APIRouter(prefix="/api/lgpd/consentimento", tags=["LGPD"])

@router.get("/listar")
async def list_consents(user: User = Depends(get_current_user)):
    """Lista todos os consentimentos do usuário"""
    consents = Consent.get_by_user(user.id)
    return {
        "consents": [
            {
                "id": c.id,
                "purpose": c.purpose,
                "description": c.description,
                "status": c.status,
                "granted_at": c.granted_at,
                "can_revoke": True
            }
            for c in consents
        ]
    }

@router.post("/conceder")
async def grant_consent(
    request: GrantConsentDTO,
    user: User = Depends(get_current_user),
    ip: str = Depends(get_client_ip)
):
    """Concede consentimento"""
    consent = Consent.create(
        user_id=user.id,
        purpose=request.purpose,
        description=request.description,
        granted_at=datetime.now(),
        status=ConsentStatus.GRANTED,
        ip_address=ip,
        user_agent=request.user_agent,
        version=1
    )
    
    # Log de auditoria
    audit_log.record(
        action="CONSENT_GRANTED",
        user_id=user.id,
        consent_id=consent.id,
        purpose=request.purpose
    )
    
    return {"message": "Consentimento concedido", "consent_id": consent.id}

@router.post("/{consent_id}/revogar")
async def revoke_consent(
    consent_id: UUID,
    user: User = Depends(get_current_user)
):
    """Revoga consentimento"""
    consent = Consent.get(consent_id)
    
    # Verificar se pertence ao usuário
    if consent.user_id != user.id:
        raise HTTPException(403, "Não autorizado")
    
    # Revogar
    consent.status = ConsentStatus.REVOKED
    consent.revoked_at = datetime.now()
    consent.save()
    
    # Parar tratamento baseado nesse consentimento
    stop_processing_based_on_consent(consent)
    
    # Log
    audit_log.record(
        action="CONSENT_REVOKED",
        user_id=user.id,
        consent_id=consent_id
    )
    
    return {"message": "Consentimento revogado"}
```

### Formulário de Consentimento

```html
<!-- Exemplo de formulário -->
<form id="consent-form">
    <h3>Consentimento para Notificações</h3>
    
    <div class="consent-box">
        <p><strong>Finalidade:</strong> Envio de alertas e notificações sobre eventos do sistema</p>
        <p><strong>Dados tratados:</strong> Email, nome</p>
        <p><strong>Duração:</strong> Enquanto você for usuário ativo</p>
        <p><strong>Controlador:</strong> GT-Vision Tecnologia</p>
        <p><strong>DPO:</strong> dpo@gtvision.com.br</p>
        <p><strong>Você pode revogar este consentimento a qualquer momento.</strong></p>
    </div>
    
    <label>
        <input type="checkbox" name="consent" required>
        Concordo em receber notificações por email
    </label>
    
    <button type="submit">Confirmar</button>
</form>
```

## 📝 Registro de Consentimento

### Informações Obrigatórias
- ✅ Quem concedeu (user_id)
- ✅ Quando concedeu (timestamp)
- ✅ Para qual finalidade (purpose)
- ✅ Qual versão do termo (version)
- ✅ Como concedeu (IP, user agent)

### Evidências
```python
class ConsentEvidence:
    consent_id: UUID
    ip_address: str
    user_agent: str
    timestamp: datetime
    form_version: int
    acceptance_method: str  # "checkbox", "button", "api"
```

## 🔄 Renovação de Consentimento

### Quando Renovar
- Mudança na finalidade
- Mudança no tratamento
- Mudança no controlador
- Após 2 anos (boa prática)

### Implementação
```python
@router.post("/{consent_id}/renovar")
async def renew_consent(
    consent_id: UUID,
    user: User = Depends(get_current_user)
):
    old_consent = Consent.get(consent_id)
    
    # Criar novo consentimento
    new_consent = Consent.create(
        user_id=user.id,
        purpose=old_consent.purpose,
        description=old_consent.description,
        granted_at=datetime.now(),
        status=ConsentStatus.GRANTED,
        version=old_consent.version + 1
    )
    
    # Expirar antigo
    old_consent.status = ConsentStatus.EXPIRED
    old_consent.save()
    
    return {"message": "Consentimento renovado", "consent_id": new_consent.id}
```

## 🚫 Revogação de Consentimento

### Efeitos da Revogação
1. ✅ Parar imediatamente o tratamento
2. ✅ Notificar sistemas dependentes
3. ✅ Registrar em log de auditoria
4. ✅ Informar o titular

### Implementação
```python
def stop_processing_based_on_consent(consent: Consent):
    """Para tratamento baseado em consentimento revogado"""
    
    if consent.purpose == "email_notifications":
        # Desabilitar notificações por email
        user = User.get(consent.user_id)
        user.email_notifications_enabled = False
        user.save()
        
    elif consent.purpose == "data_sharing":
        # Parar compartilhamento com terceiros
        stop_data_sharing(consent.user_id)
        
    # Log
    logger.info(f"Processing stopped for consent {consent.id}")
```

## 📊 Dashboard de Consentimentos

```python
@router.get("/dashboard")
async def consent_dashboard(admin: User = Depends(require_admin)):
    """Dashboard de consentimentos (apenas admin)"""
    
    total = Consent.count()
    granted = Consent.count_by_status(ConsentStatus.GRANTED)
    revoked = Consent.count_by_status(ConsentStatus.REVOKED)
    
    by_purpose = Consent.group_by_purpose()
    
    return {
        "total": total,
        "granted": granted,
        "revoked": revoked,
        "revocation_rate": revoked / total if total > 0 else 0,
        "by_purpose": by_purpose
    }
```

## ⚠️ Erros Comuns

### ❌ Consentimento genérico
```python
# ERRADO
consent = "Concordo com os termos de uso"
```

### ✅ Consentimento específico
```python
# CORRETO
consent = {
    "purpose": "Envio de notificações por email",
    "description": "Você receberá alertas sobre eventos do sistema",
    "data": ["email", "nome"]
}
```

### ❌ Checkbox pré-marcado
```html
<!-- ERRADO -->
<input type="checkbox" name="consent" checked>
```

### ✅ Opt-in explícito
```html
<!-- CORRETO -->
<input type="checkbox" name="consent" required>
```

### ❌ Consentimento como condição
```python
# ERRADO
if not user.has_consent("marketing"):
    raise Exception("Você precisa aceitar marketing para usar o sistema")
```

### ✅ Consentimento opcional
```python
# CORRETO
if user.has_consent("marketing"):
    send_marketing_email(user)
else:
    logger.info(f"User {user.id} has not consented to marketing")
```

## ✅ Checklist de Consentimento

- [ ] Consentimento livre (não obrigatório)
- [ ] Finalidade específica e clara
- [ ] Linguagem simples e acessível
- [ ] Destacado de outros termos
- [ ] Opt-in explícito (não pré-marcado)
- [ ] Registro de evidências (IP, timestamp)
- [ ] Possibilidade de revogação
- [ ] Revogação com efeito imediato
- [ ] Renovação periódica (2 anos)
- [ ] Dashboard de monitoramento
