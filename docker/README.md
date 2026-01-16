# Docker Compose - Estrutura

## 📋 Arquivos Disponíveis

### 1. `docker-compose.yml` (Produção)
**Uso**: Deploy completo em produção  
**Quando usar**: AWS, servidor de produção  
**Inclui**: Tudo (HAProxy, Kong, Django, FastAPI, todos os serviços)

```bash
docker-compose up -d
```

### 2. `docker-compose.dev.yml` (Desenvolvimento - Infraestrutura)
**Uso**: Desenvolvimento local (backend roda fora do Docker)  
**Quando usar**: Desenvolvimento diário, debugging  
**Inclui**: Apenas infraestrutura (PostgreSQL, Redis, RabbitMQ, MinIO, MediaMTX, Observabilidade)  
**NÃO inclui**: HAProxy, Kong, Django, FastAPI

```bash
# Iniciar infraestrutura
docker-compose -f docker-compose.dev.yml up -d

# Rodar backend localmente
poetry run python manage.py runserver
poetry run uvicorn src.streaming.infrastructure.web.main:app --reload --port 8001
```

### 3. `docker-compose.test.yml` (Testes E2E)
**Uso**: Testes completos com HAProxy + Kong  
**Quando usar**: Validar Sprint 13, testes E2E  
**Inclui**: Tudo exceto frontend (HAProxy, Kong, FastAPI, infraestrutura, observabilidade)

```bash
docker-compose -f docker-compose.test.yml up -d
```

---

## 🎯 Quando Usar Cada Um

| Cenário | Arquivo | Comando |
|---------|---------|---------|
| **Desenvolvimento diário** | `docker-compose.dev.yml` | `docker-compose -f docker-compose.dev.yml up -d` |
| **Testar HAProxy/Kong** | `docker-compose.test.yml` | `docker-compose -f docker-compose.test.yml up -d` |
| **Deploy produção** | `docker-compose.yml` | `docker-compose up -d` |

---

## 📊 Comparação

| Serviço | dev.yml | test.yml | yml (prod) |
|---------|---------|----------|------------|
| PostgreSQL | ✅ | ✅ | ✅ |
| Redis | ✅ | ✅ | ✅ |
| RabbitMQ | ✅ | ✅ | ✅ |
| MinIO | ✅ | ✅ | ✅ |
| MediaMTX | ✅ | ✅ | ✅ |
| Prometheus | ✅ | ✅ | ✅ |
| Grafana | ✅ | ✅ | ✅ |
| ELK Stack | ✅ | ✅ | ✅ |
| **Streaming API** | ✅ | ✅ | ✅ |
| **HAProxy** | ❌ | ✅ | ✅ |
| **Kong** | ❌ | ✅ | ✅ |
| **Django** | ❌ | ❌ | ✅ |
| **Frontend** | ❌ | ❌ | ✅ |

---

## 🚀 Scripts Úteis

### Desenvolvimento
```bash
# Iniciar infraestrutura
scripts\start-dev.bat

# Parar
docker-compose -f docker-compose.dev.yml down
```

### Testes E2E
```bash
# Iniciar stack de testes
scripts\start-test.bat

# Executar testes
scripts\test-sprint13.bat

# Parar
docker-compose -f docker-compose.test.yml down
```

### Produção
```bash
# Iniciar tudo
docker-compose up -d

# Parar
docker-compose down
```

---

## 📝 Notas

- **dev.yml**: Mais rápido para desenvolvimento (backend local)
- **test.yml**: Para validar integração HAProxy/Kong
- **yml**: Deploy completo (ainda não finalizado - falta Django e Frontend)

---

## 🔄 Migração

### De dev.yml para test.yml
```bash
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.test.yml up -d
```

### De test.yml para dev.yml
```bash
docker-compose -f docker-compose.test.yml down
docker-compose -f docker-compose.dev.yml up -d
```
