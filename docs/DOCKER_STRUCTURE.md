# Docker Compose - Estrutura Final Sprint 13

## ✅ Arquivos Criados

### 1. `docker-compose.dev.yml` ⚙️
**Propósito**: Desenvolvimento diário  
**Status**: ✅ Rodando atualmente  
**Inclui**: Infraestrutura apenas  
**Backend**: Roda localmente (Poetry)

**Serviços** (15):
- PostgreSQL, Redis, RabbitMQ, MinIO, MediaMTX
- Streaming API (container)
- Prometheus, Grafana, Alertmanager
- Node/PostgreSQL/Redis Exporters
- Elasticsearch, Logstash, Kibana

**Comando**:
```bash
docker-compose -f docker-compose.dev.yml up -d
# ou
scripts\start-dev.bat
```

---

### 2. `docker-compose.test.yml` 🧪
**Propósito**: Testes E2E com HAProxy + Kong  
**Status**: ✅ Pronto para usar  
**Inclui**: Infraestrutura + HAProxy + Kong  
**Backend**: Streaming API em container

**Serviços** (17):
- Todos do dev.yml +
- **HAProxy** (porta 80, 8404)
- **Kong** (porta 8000, 8443)

**Comando**:
```bash
docker-compose -f docker-compose.test.yml up -d
# ou
scripts\start-test.bat
```

---

### 3. `docker-compose.yml` 🚀
**Propósito**: Produção (futuro)  
**Status**: ⏳ Ainda não criado  
**Inclui**: Stack completa (HAProxy, Kong, Django, FastAPI, Frontend)  
**Quando**: Sprint 15+ (após integração frontend)

---

## 📊 Comparação Rápida

| Componente | dev.yml | test.yml | yml (prod) |
|------------|---------|----------|------------|
| Infraestrutura | ✅ | ✅ | ✅ |
| Streaming API | ✅ | ✅ | ✅ |
| Observabilidade | ✅ | ✅ | ✅ |
| **HAProxy** | ❌ | ✅ | ✅ |
| **Kong** | ❌ | ✅ | ✅ |
| Django | ❌ | ❌ | ✅ |
| Frontend | ❌ | ❌ | ✅ |

---

## 🎯 Quando Usar

### Desenvolvimento Diário → `dev.yml`
```bash
scripts\start-dev.bat
poetry run python manage.py runserver
poetry run uvicorn src.streaming.infrastructure.web.main:app --reload --port 8001
```

### Testar Sprint 13 → `test.yml`
```bash
scripts\start-test.bat
curl http://localhost:8404/stats  # HAProxy
curl http://localhost:8000         # Kong
curl http://localhost/api/streaming/health  # Via HAProxy
```

### Deploy Produção → `yml` (futuro)
```bash
docker-compose up -d
```

---

## 📁 Arquivos de Configuração

### HAProxy
- `haproxy/haproxy.cfg` - Original (com frontend)
- `haproxy/haproxy.prod.cfg` - Produção (SSL, security headers)
- `haproxy/haproxy.simple.cfg` - Testes (sem frontend) ✅ Usado em test.yml

### Kong
- `kong/kong.yml` - Original
- `kong/kong.prod.yml` - Produção (JWT, RBAC)
- `kong/kong.simple.yml` - Testes (básico) ✅ Usado em test.yml

---

## 🚀 Scripts Disponíveis

### Desenvolvimento
- `scripts\start-dev.bat` - Inicia dev.yml
- `scripts\start-and-test.bat` - Inicia dev.yml + smoke tests

### Testes
- `scripts\start-test.bat` - Inicia test.yml
- `scripts\test-sprint13.bat` - Executa testes Sprint 13
- `scripts\validate-stack.bat` - Validação rápida

---

## 🔄 Migração Entre Ambientes

### Dev → Test
```bash
docker-compose -f docker-compose.dev.yml down
scripts\start-test.bat
```

### Test → Dev
```bash
docker-compose -f docker-compose.test.yml down
scripts\start-dev.bat
```

---

## ✅ Status Atual

**Rodando**: `docker-compose.dev.yml`  
**Validado**: ✅ 15/15 serviços UP  
**Próximo**: Testar `docker-compose.test.yml` com HAProxy + Kong

---

## 📝 Notas Importantes

1. **dev.yml**: Mais rápido, ideal para desenvolvimento
2. **test.yml**: Para validar HAProxy/Kong antes de produção
3. **yml**: Será criado na Sprint 15 (integração frontend)

4. **Portas**:
   - dev.yml: 8001 (Streaming direto)
   - test.yml: 80 (HAProxy), 8000 (Kong), 8001 (Streaming)

5. **Networks**:
   - dev.yml: Sem networks (default)
   - test.yml: Network `backend`

---

**Criado**: 2025-01-16  
**Sprint**: 13 - Logs e Segurança  
**Status**: ✅ Estrutura completa e documentada
