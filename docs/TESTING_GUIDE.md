# Guia de Testes - Sprint 13

## 🚀 Quick Start

### 1. Iniciar Stack Completa

```bash
# Iniciar todos os serviços
docker-compose -f docker-compose.dev.yml up -d

# Aguardar serviços ficarem prontos (30-60s)
timeout /t 60

# Verificar status
docker-compose -f docker-compose.dev.yml ps
```

### 2. Validação Rápida

```bash
# Smoke tests automatizados
scripts\validate-stack.bat

# Ou manualmente
poetry run python tests/smoke_test.py
```

### 3. Executar Testes Completos

```bash
# Todos os testes Sprint 13
scripts\test-sprint13-docker.bat

# Ou individualmente
poetry run pytest tests/integration/test_haproxy.py -v
poetry run pytest tests/integration/test_kong.py -v
poetry run pytest tests/e2e/test_full_flow.py -v -m e2e
```

---

## 📋 Checklist de Validação

### Serviços Base
- [ ] PostgreSQL rodando (porta 5432)
- [ ] Redis rodando (porta 6379)
- [ ] RabbitMQ rodando (porta 5672, 15672)
- [ ] MinIO rodando (porta 9000, 9001)
- [ ] MediaMTX rodando (porta 8554, 8888, 8889)

### APIs
- [ ] Streaming API rodando (porta 8001)
- [ ] Health endpoint: http://localhost:8001/health
- [ ] Docs endpoint: http://localhost:8001/docs
- [ ] Metrics endpoint: http://localhost:8001/metrics

### Observabilidade
- [ ] Prometheus rodando (porta 9090)
- [ ] Grafana rodando (porta 3000)
- [ ] Elasticsearch rodando (porta 9200)
- [ ] Logstash rodando (porta 5000)
- [ ] Kibana rodando (porta 5601)

### Testes
- [ ] 5 testes HAProxy passando
- [ ] 6 testes Kong passando
- [ ] 8 testes E2E passando
- [ ] Smoke tests passando

---

## 🧪 Testes Detalhados

### HAProxy (5 testes)

```bash
poetry run pytest tests/integration/test_haproxy.py -v
```

**Testes**:
1. `test_stats_available` - Dashboard de stats
2. `test_health_check` - Endpoint /health
3. `test_routes_to_streaming` - Roteamento para FastAPI
4. `test_rate_limiting` - Rate limit (429)
5. `test_security_headers` - Headers de segurança

**Esperado**: 5/5 passing ✅

### Kong Gateway (6 testes)

```bash
poetry run pytest tests/integration/test_kong.py -v
```

**Testes**:
1. `test_kong_health` - Kong health check
2. `test_kong_routes_admin` - Roteamento /api/admin
3. `test_kong_routes_streaming` - Roteamento /api/streaming
4. `test_kong_rate_limiting` - Rate limit (429)
5. `test_kong_cors_headers` - CORS headers
6. `test_kong_jwt_required` - JWT obrigatório (401)

**Esperado**: 6/6 passing ✅

### E2E Full Flow (8 testes)

```bash
poetry run pytest tests/e2e/test_full_flow.py -v -m e2e
```

**Testes**:
1. `test_create_camera_and_stream` - Django → FastAPI → MediaMTX
2. `test_lpr_detection_flow` - Webhook LPR → Buscar
3. `test_security_flow` - 401, 429, audit
4. `test_observability` - Prometheus, Grafana, ELK
5. `test_rabbitmq_connection` - RabbitMQ API
6. `test_mediamtx_connection` - MediaMTX
7. `test_minio_connection` - MinIO health
8. `test_api_response_time` - Latência <200ms

**Esperado**: 8/8 passing ✅

---

## 🔍 Troubleshooting

### Serviços não iniciam

```bash
# Ver logs
docker-compose -f docker-compose.dev.yml logs

# Reiniciar serviço específico
docker-compose -f docker-compose.dev.yml restart streaming

# Rebuild
docker-compose -f docker-compose.dev.yml up -d --build
```

### Testes falhando

**Connection Refused**:
```bash
# Aguardar mais tempo
timeout /t 30

# Verificar se serviço está UP
docker-compose -f docker-compose.dev.yml ps
```

**401 Unauthorized**:
```bash
# Verificar se JWT está configurado
# Verificar se token está válido
```

**429 Too Many Requests**:
```bash
# Aguardar rate limit resetar (10s)
timeout /t 10
```

### Logs

```bash
# Todos os logs
docker-compose -f docker-compose.dev.yml logs -f

# Serviço específico
docker-compose -f docker-compose.dev.yml logs -f streaming

# Últimas 50 linhas
docker-compose -f docker-compose.dev.yml logs --tail=50 streaming
```

---

## 📊 Endpoints para Teste Manual

### Streaming API
- Health: http://localhost:8001/health
- Docs: http://localhost:8001/docs
- Metrics: http://localhost:8001/metrics

### Observabilidade
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)
- Kibana: http://localhost:5601

### Infraestrutura
- RabbitMQ: http://localhost:15672 (gtvision/gtvision_password)
- MinIO: http://localhost:9001 (minioadmin/minioadmin)

---

## 🎯 Testes Manuais

### 1. Testar Health Check

```bash
curl http://localhost:8001/health
# Esperado: {"status": "ok"}
```

### 2. Testar Metrics

```bash
curl http://localhost:8001/metrics
# Esperado: Métricas Prometheus
```

### 3. Testar Rate Limiting

```bash
# Fazer 15 requests rápidos
for /L %i in (1,1,15) do curl http://localhost:8001/health

# Esperado: Alguns 429 (Too Many Requests)
```

### 4. Testar JWT

```bash
# Sem token (deve retornar 401)
curl http://localhost:8000/api/admin/users

# Com token
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/admin/users
```

### 5. Testar CORS

```bash
curl -H "Origin: http://localhost:5173" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS \
     http://localhost:8000/api/streaming/health

# Esperado: Access-Control-Allow-Origin header
```

---

## 📈 Métricas de Sucesso

### Performance
- ✅ API response time <200ms
- ✅ Health check <50ms
- ✅ Metrics endpoint <100ms

### Disponibilidade
- ✅ Todos os serviços UP
- ✅ Health checks passando
- ✅ 0 erros nos logs

### Testes
- ✅ 48/48 testes passando
- ✅ Cobertura >90%
- ✅ 0 testes flaky

---

## 🔄 Comandos Úteis

```bash
# Iniciar stack
docker-compose -f docker-compose.dev.yml up -d

# Parar stack
docker-compose -f docker-compose.dev.yml down

# Parar e limpar volumes
docker-compose -f docker-compose.dev.yml down -v

# Ver logs em tempo real
docker-compose -f docker-compose.dev.yml logs -f

# Executar comando em container
docker-compose -f docker-compose.dev.yml exec streaming bash

# Ver uso de recursos
docker stats

# Limpar tudo
docker-compose -f docker-compose.dev.yml down -v --rmi all
```

---

## ✅ Resultado Esperado

Após executar todos os testes:

```
========================================
GT-Vision VMS - Sprint 13 Tests
========================================

[1/5] HAProxy Tests:           5/5 passing ✅
[2/5] Kong Tests:              6/6 passing ✅
[3/5] E2E Tests:               8/8 passing ✅
[4/5] Smoke Tests:             OK ✅
[5/5] Services Health:         10/10 UP ✅

========================================
SUCESSO! Sprint 13 100% validada
========================================
```

---

**Tempo estimado**: 5-10 minutos (incluindo inicialização dos serviços)
