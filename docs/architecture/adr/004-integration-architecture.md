# ADR 004: Arquitetura de Integração Final

## Status
Aceito | Sprint 11 (Jan 2025)

## Contexto
Após implementar os 4 bounded contexts (Admin, Cidades, Streaming, AI), precisamos definir como eles se integram de forma robusta, escalável e manutenível.

### Requisitos:
- Comunicação síncrona e assíncrona
- Baixo acoplamento entre contexts
- Alta disponibilidade
- Observabilidade completa
- Segurança em todas as camadas

## Decisão

### 1. Stack de Integração

#### Proxy & Gateway
- **HAProxy**: Load balancer, SSL termination, rate limiting
- **Kong Gateway**: API Gateway, autenticação, roteamento

#### Backend
- **Django 5.0** (Admin + Cidades): REST API, JWT auth
- **FastAPI** (Streaming + AI): Async API, WebSocket

#### Infraestrutura
- **PostgreSQL 15**: Database principal
- **Redis 7**: Cache distribuído
- **RabbitMQ 3**: Message broker
- **MinIO**: S3-compatible storage
- **MediaMTX**: Streaming server

#### Observabilidade
- **Prometheus + Grafana**: Métricas
- **ELK Stack**: Logs centralizados

### 2. Padrões de Comunicação

#### Síncrona (REST API)
```
Cliente → HAProxy → Kong → Backend → Database
```

**Casos de uso:**
- Autenticação e autorização
- CRUD de entidades
- Consultas imediatas
- Validações síncronas

**Implementação:**
- HTTP/REST via Kong Gateway
- JWT para autenticação
- Rate limiting no HAProxy e Kong
- Timeout: 30s

#### Assíncrona (RabbitMQ)
```
Context A → RabbitMQ → Context B
```

**Casos de uso:**
- Eventos de domínio
- Processamento em background
- Notificações
- Eventual consistency

**Implementação:**
- RabbitMQ com exchanges e queues
- Retry automático (3x)
- Dead letter queue
- Idempotência garantida

### 3. Eventos de Domínio

#### Cidades → Streaming
- `camera.created`: Nova câmera cadastrada
- `camera.updated`: Câmera atualizada
- `camera.deleted`: Câmera removida
- `city.storage_plan_changed`: Plano alterado

#### Streaming → AI
- `recording.started`: Gravação iniciada
- `recording.stopped`: Gravação finalizada
- `stream.health_check`: Status do stream

#### AI → Cidades
- `lpr.detected`: Placa detectada
- `alert.triggered`: Alerta gerado
- `analytics.daily_report`: Relatório diário

### 4. Shared Kernel

**Localização:** `src/shared_kernel/`

**Conteúdo:**
- Value Objects comuns (Email, CPF, CNPJ)
- Exceções base
- Interfaces de repositórios
- Event bus abstrato
- Logging configurado
- Métricas base

**Regra:** Apenas código estável e genérico

### 5. Anti-Corruption Layer (ACL)

Cada context tem ACL para proteger seu domínio:

```python
# streaming/infrastructure/acl/cidades_acl.py
class CidadesACL:
    """Traduz dados de Cidades para Streaming"""
    
    def to_camera_entity(self, cidades_camera: dict) -> Camera:
        # Converte formato externo para entidade interna
        pass
```

### 6. Segurança

#### Camada 1: HAProxy
- Rate limiting: 100 req/s por IP
- SSL termination
- DDoS protection

#### Camada 2: Kong
- JWT validation
- API key management
- Rate limiting por usuário: 60 req/min

#### Camada 3: Backend
- RBAC (Role-Based Access Control)
- Input validation (Pydantic/DRF)
- SQL injection prevention
- XSS protection

#### Camada 4: Database
- Prepared statements
- Encryption at rest
- Connection pooling
- Least privilege

### 7. Observabilidade

#### Métricas (Prometheus)
```python
# Métricas coletadas
- http_requests_total
- http_request_duration_seconds
- streaming_active_cameras
- ai_lpr_detections_total
- database_connections_active
```

#### Logs (ELK)
```json
{
  "timestamp": "2025-01-16T10:30:00Z",
  "level": "INFO",
  "context": "streaming",
  "correlation_id": "abc-123",
  "message": "Stream started",
  "camera_id": "cam-001"
}
```

#### Tracing
- Correlation ID em todas requisições
- Propagação entre contexts
- Tempo de resposta por camada

### 8. Resiliência

#### Circuit Breaker
```python
@circuit_breaker(failure_threshold=5, timeout=60)
async def call_external_service():
    pass
```

#### Retry Policy
- Tentativas: 3x
- Backoff: Exponencial (1s, 2s, 4s)
- Timeout: 30s

#### Fallback
- Cache Redis para dados críticos
- Resposta degradada quando serviço offline
- Queue para processar depois

### 9. Performance

#### Targets
- API latência: < 100ms (p95)
- Streaming latência: < 2s (HLS)
- Throughput: 1000 req/s
- Câmeras simultâneas: 100+

#### Otimizações
- Connection pooling (PostgreSQL)
- Cache Redis (TTL inteligente)
- Async I/O (FastAPI)
- Índices otimizados
- Query optimization

### 10. Deployment

#### Desenvolvimento
```bash
# Infraestrutura
docker-compose -f docker-compose.dev.yml up -d

# Backend Django
poetry run python manage.py runserver

# Backend FastAPI
cd src/streaming
poetry run uvicorn infrastructure.web.main:app --reload --port 8001
```

#### Produção
```bash
# Docker Compose
docker-compose up -d

# Kubernetes (futuro)
kubectl apply -f k8s/

# Terraform (AWS)
terraform apply
```

## Consequências

### Positivas
✅ Baixo acoplamento entre contexts
✅ Alta disponibilidade (load balancing)
✅ Escalabilidade horizontal
✅ Observabilidade completa
✅ Segurança em camadas
✅ Resiliência (retry, circuit breaker)
✅ Performance otimizada
✅ Fácil de debugar (correlation ID)

### Negativas
❌ Complexidade operacional aumentada
❌ Mais componentes para monitorar
❌ Eventual consistency (eventos)
❌ Overhead de rede (múltiplos serviços)
❌ Custo de infraestrutura maior

### Mitigações
- Automação com Docker Compose
- Monitoramento proativo (alertas)
- Documentação completa
- Testes de integração robustos
- Runbooks para troubleshooting

## Alternativas Consideradas

### 1. Comunicação Direta entre Contexts
❌ Alto acoplamento
❌ Difícil de escalar
❌ Sem observabilidade centralizada

### 2. API Gateway Único (sem HAProxy)
❌ Single point of failure
❌ Sem load balancing
❌ Menos flexibilidade

### 3. Kafka ao invés de RabbitMQ
❌ Over-engineering para volume atual
❌ Complexidade operacional alta
❌ Custo maior

### 4. Microserviços Completos
❌ Complexidade prematura
❌ Overhead de comunicação
❌ Difícil de debugar

## Métricas de Sucesso

### Técnicas
- Uptime: > 99.9%
- Latência API: < 100ms (p95)
- Taxa de erro: < 0.1%
- Cobertura de testes: > 90%

### Negócio
- 1000 câmeras simultâneas
- 100 prefeituras ativas
- 10k eventos LPR/dia
- 0 incidentes críticos

## Próximos Passos

### Sprint 12
- [ ] Implementar circuit breaker
- [ ] Adicionar tracing distribuído
- [ ] Otimizar queries N+1
- [ ] Testes de carga (Locust)

### Sprint 13
- [ ] CDN para HLS
- [ ] Cache warming
- [ ] Auto-scaling (Kubernetes)
- [ ] Disaster recovery plan

## Referências
- [Microservices Patterns - Chris Richardson](https://microservices.io/patterns/)
- [Building Microservices - Sam Newman](https://samnewman.io/books/building_microservices/)
- [Kong Gateway Docs](https://docs.konghq.com/)
- [RabbitMQ Best Practices](https://www.rabbitmq.com/best-practices.html)
