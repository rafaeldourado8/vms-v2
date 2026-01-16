# 8️⃣ Incidentes de Segurança

Gestão de incidentes de segurança e vazamento de dados (Art. 48 da LGPD).

## 📋 Definição de Incidente

Qualquer evento adverso confirmado relacionado à violação de dados pessoais:
- Acesso não autorizado
- Destruição acidental ou ilícita
- Perda, alteração ou divulgação não autorizada
- Qualquer forma de tratamento inadequado

## 🚨 Classificação de Incidentes

### Nível 1 - Baixo Risco
**Características**:
- Dados não sensíveis
- Impacto limitado
- Poucos titulares afetados (<10)

**Exemplos**:
- Acesso não autorizado a dados públicos
- Erro de configuração sem exposição

**Ação**: Correção interna, sem notificação à ANPD.

### Nível 2 - Médio Risco
**Características**:
- Dados pessoais comuns
- Impacto moderado
- Número moderado de titulares (10-100)

**Exemplos**:
- Vazamento de emails e nomes
- Acesso não autorizado a logs

**Ação**: Correção + notificação aos titulares.

### Nível 3 - Alto Risco
**Características**:
- Dados sensíveis
- Impacto significativo
- Grande número de titulares (>100)

**Exemplos**:
- Vazamento de CPFs
- Acesso não autorizado a imagens
- Ransomware

**Ação**: Correção + notificação à ANPD + notificação aos titulares.

### Nível 4 - Crítico
**Características**:
- Dados sensíveis em larga escala
- Risco grave aos titulares
- Exposição pública

**Exemplos**:
- Vazamento massivo de dados
- Publicação de dados sensíveis
- Ataque com danos irreversíveis

**Ação**: Todas as anteriores + comunicação pública + medidas urgentes.

## ⏱️ Prazos

### Notificação à ANPD
- **Prazo**: Prazo razoável (geralmente 2-5 dias úteis)
- **Quando**: Incidentes de alto risco ou críticos

### Notificação aos Titulares
- **Prazo**: Prazo razoável (geralmente 2-5 dias úteis)
- **Quando**: Risco ou dano relevante aos titulares

## 📝 Conteúdo da Notificação

### À ANPD (Art. 48, § 1º)
1. Descrição do incidente
2. Dados pessoais afetados
3. Titulares afetados
4. Medidas técnicas e de segurança
5. Riscos aos titulares
6. Motivos da demora (se aplicável)
7. Medidas adotadas para reverter ou mitigar

### Aos Titulares (Art. 48, § 2º)
1. Descrição em linguagem clara
2. Dados afetados
3. Medidas adotadas
4. Riscos ao titular
5. Medidas de segurança recomendadas
6. Contato do DPO

## 💻 Implementação

### Modelo de Incidente

```python
from enum import Enum
from datetime import datetime
from uuid import UUID

class IncidentSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentStatus(str, Enum):
    DETECTED = "detected"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    RESOLVED = "resolved"
    CLOSED = "closed"

class SecurityIncident:
    id: UUID
    title: str
    description: str
    severity: IncidentSeverity
    status: IncidentStatus
    detected_at: datetime
    reported_at: Optional[datetime]
    resolved_at: Optional[datetime]
    affected_users: List[UUID]
    affected_data_types: List[str]
    root_cause: Optional[str]
    mitigation_actions: List[str]
    notified_anpd: bool
    notified_users: bool
    responsible_user_id: UUID
```

### Serviço de Gestão de Incidentes

```python
class IncidentManagementService:
    def __init__(self):
        self.notification_service = NotificationService()
        self.anpd_service = ANPDNotificationService()
    
    async def report_incident(
        self,
        title: str,
        description: str,
        severity: IncidentSeverity,
        affected_users: List[UUID],
        affected_data_types: List[str]
    ) -> SecurityIncident:
        """Registra novo incidente"""
        
        # Criar incidente
        incident = SecurityIncident.create(
            title=title,
            description=description,
            severity=severity,
            status=IncidentStatus.DETECTED,
            detected_at=datetime.now(),
            affected_users=affected_users,
            affected_data_types=affected_data_types
        )
        
        # Notificar DPO imediatamente
        await self.notification_service.notify_dpo(incident)
        
        # Se alto risco ou crítico, iniciar processo de notificação
        if severity in [IncidentSeverity.HIGH, IncidentSeverity.CRITICAL]:
            await self._initiate_notification_process(incident)
        
        # Log
        logger.critical(f"Security incident reported: {incident.id}")
        
        return incident
    
    async def _initiate_notification_process(self, incident: SecurityIncident):
        """Inicia processo de notificação à ANPD e titulares"""
        
        # Notificar ANPD
        if incident.severity in [IncidentSeverity.HIGH, IncidentSeverity.CRITICAL]:
            await self.anpd_service.notify(incident)
            incident.notified_anpd = True
            incident.reported_at = datetime.now()
        
        # Notificar titulares
        if len(incident.affected_users) > 0:
            await self._notify_affected_users(incident)
            incident.notified_users = True
    
    async def _notify_affected_users(self, incident: SecurityIncident):
        """Notifica usuários afetados"""
        
        for user_id in incident.affected_users:
            user = User.get(user_id)
            
            message = f"""
            Prezado(a) {user.name},
            
            Informamos que ocorreu um incidente de segurança que pode ter afetado seus dados pessoais.
            
            Dados afetados: {', '.join(incident.affected_data_types)}
            Data do incidente: {incident.detected_at.strftime('%d/%m/%Y')}
            
            Medidas adotadas:
            {self._format_mitigation_actions(incident)}
            
            Recomendações:
            - Altere sua senha imediatamente
            - Monitore suas contas
            - Fique atento a comunicações suspeitas
            
            Para mais informações, entre em contato com nosso DPO:
            Email: dpo@gtvision.com.br
            Telefone: (11) 1234-5678
            
            Atenciosamente,
            Equipe GT-Vision
            """
            
            await self.notification_service.send_email(
                to=user.email,
                subject="Notificação de Incidente de Segurança",
                body=message
            )
    
    async def update_incident(
        self,
        incident_id: UUID,
        status: IncidentStatus,
        root_cause: Optional[str] = None,
        mitigation_actions: Optional[List[str]] = None
    ):
        """Atualiza status do incidente"""
        
        incident = SecurityIncident.get(incident_id)
        incident.status = status
        
        if root_cause:
            incident.root_cause = root_cause
        
        if mitigation_actions:
            incident.mitigation_actions = mitigation_actions
        
        if status == IncidentStatus.RESOLVED:
            incident.resolved_at = datetime.now()
        
        incident.save()
        
        # Log
        audit_log.record(
            action="INCIDENT_UPDATED",
            resource_id=incident_id,
            details={"status": status}
        )
```

### Endpoint de Incidentes

```python
@router.post("/api/incidents")
async def report_incident(
    request: ReportIncidentDTO,
    admin: User = Depends(require_admin)
):
    """Registra novo incidente (apenas admin)"""
    
    service = IncidentManagementService()
    incident = await service.report_incident(
        title=request.title,
        description=request.description,
        severity=request.severity,
        affected_users=request.affected_users,
        affected_data_types=request.affected_data_types
    )
    
    return {"incident_id": incident.id, "status": incident.status}

@router.get("/api/incidents")
async def list_incidents(
    admin: User = Depends(require_admin)
):
    """Lista todos os incidentes (apenas admin)"""
    
    incidents = SecurityIncident.all()
    return {
        "incidents": [
            {
                "id": i.id,
                "title": i.title,
                "severity": i.severity,
                "status": i.status,
                "detected_at": i.detected_at,
                "affected_users_count": len(i.affected_users)
            }
            for i in incidents
        ]
    }

@router.patch("/api/incidents/{incident_id}")
async def update_incident(
    incident_id: UUID,
    request: UpdateIncidentDTO,
    admin: User = Depends(require_admin)
):
    """Atualiza incidente (apenas admin)"""
    
    service = IncidentManagementService()
    await service.update_incident(
        incident_id=incident_id,
        status=request.status,
        root_cause=request.root_cause,
        mitigation_actions=request.mitigation_actions
    )
    
    return {"message": "Incidente atualizado"}
```

## 📊 Dashboard de Incidentes

```python
@router.get("/api/incidents/dashboard")
async def incidents_dashboard(admin: User = Depends(require_admin)):
    """Dashboard de incidentes"""
    
    total = SecurityIncident.count()
    by_severity = SecurityIncident.group_by_severity()
    by_status = SecurityIncident.group_by_status()
    
    # Tempo médio de resolução
    resolved = SecurityIncident.filter(status=IncidentStatus.RESOLVED)
    avg_resolution_time = sum(
        (i.resolved_at - i.detected_at).total_seconds()
        for i in resolved
    ) / len(resolved) if resolved else 0
    
    return {
        "total": total,
        "by_severity": by_severity,
        "by_status": by_status,
        "avg_resolution_time_hours": avg_resolution_time / 3600,
        "open_incidents": SecurityIncident.count_by_status(IncidentStatus.INVESTIGATING)
    }
```

## 🔍 Detecção de Incidentes

### Monitoramento Automático

```python
@celery.task
def monitor_security_incidents():
    """Task para detectar incidentes automaticamente"""
    
    # 1. Múltiplas tentativas de login falhadas
    failed_logins = AuditLog.filter(
        action="LOGIN_FAILED",
        timestamp__gte=datetime.now() - timedelta(minutes=5)
    ).group_by("user_id")
    
    for user_id, count in failed_logins.items():
        if count >= 5:
            await report_incident(
                title="Múltiplas tentativas de login falhadas",
                description=f"Usuário {user_id} teve {count} tentativas falhadas",
                severity=IncidentSeverity.MEDIUM,
                affected_users=[user_id],
                affected_data_types=["credentials"]
            )
    
    # 2. Acesso a dados sensíveis fora do horário
    after_hours_access = AuditLog.filter(
        action="DATA_ACCESS",
        timestamp__hour__in=[22, 23, 0, 1, 2, 3, 4, 5]
    )
    
    if after_hours_access.count() > 0:
        # Investigar
        pass
    
    # 3. Download massivo de dados
    bulk_downloads = AuditLog.filter(
        action="DATA_EXPORT",
        timestamp__gte=datetime.now() - timedelta(hours=1)
    ).group_by("user_id")
    
    for user_id, count in bulk_downloads.items():
        if count >= 10:
            await report_incident(
                title="Download massivo de dados",
                description=f"Usuário {user_id} exportou {count} vezes em 1 hora",
                severity=IncidentSeverity.HIGH,
                affected_users=[user_id],
                affected_data_types=["personal_data"]
            )
```

## 📋 Plano de Resposta a Incidentes

### Fase 1: Detecção (0-1h)
1. ✅ Identificar o incidente
2. ✅ Classificar severidade
3. ✅ Notificar DPO
4. ✅ Registrar no sistema

### Fase 2: Contenção (1-4h)
1. ✅ Isolar sistemas afetados
2. ✅ Bloquear acessos não autorizados
3. ✅ Preservar evidências
4. ✅ Avaliar extensão do dano

### Fase 3: Investigação (4-24h)
1. ✅ Identificar causa raiz
2. ✅ Determinar dados afetados
3. ✅ Identificar titulares afetados
4. ✅ Avaliar riscos

### Fase 4: Notificação (24-48h)
1. ✅ Notificar ANPD (se alto risco)
2. ✅ Notificar titulares afetados
3. ✅ Documentar notificações

### Fase 5: Recuperação (48h+)
1. ✅ Implementar correções
2. ✅ Restaurar sistemas
3. ✅ Validar segurança
4. ✅ Monitorar

### Fase 6: Lições Aprendidas
1. ✅ Análise pós-incidente
2. ✅ Atualizar procedimentos
3. ✅ Treinar equipe
4. ✅ Melhorar controles

## ✅ Checklist de Incidentes

- [ ] Plano de resposta documentado
- [ ] Equipe de resposta definida
- [ ] Contatos de emergência atualizados
- [ ] Processo de notificação à ANPD
- [ ] Template de notificação aos titulares
- [ ] Sistema de registro de incidentes
- [ ] Monitoramento automático
- [ ] Testes periódicos do plano
- [ ] Análise pós-incidente
- [ ] Treinamento da equipe
