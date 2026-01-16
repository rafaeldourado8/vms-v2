# ⚠️ COMANDOS CORRETOS - Sprint 11

## ❌ ERRADO (O que você fez)

```bash
docker-compose up          # ERRADO! Usa docker-compose.yml (produção)
docker-compose down -v     # Para produção, não dev
```

Isso tenta iniciar **15 serviços** incluindo Kong, HAProxy, ELK, Grafana, etc.

## ✅ CORRETO (Sprint 11 - Desenvolvimento Local)

### Iniciar Infraestrutura (5 serviços)

```bash
# Opção 1: Script automatizado
scripts\start-infra.bat

# Opção 2: Comando direto
docker-compose -f docker-compose.dev.yml up -d
```

### Ver Status

```bash
docker-compose -f docker-compose.dev.yml ps
```

### Ver Logs

```bash
# Todos os serviços
docker-compose -f docker-compose.dev.yml logs -f

# Apenas MediaMTX
docker-compose -f docker-compose.dev.yml logs -f mediamtx
```

### Parar Infraestrutura

```bash
# Opção 1: Script
scripts\stop-infra.bat

# Opção 2: Comando direto
docker-compose -f docker-compose.dev.yml down
```

### Limpar Tudo (volumes também)

```bash
docker-compose -f docker-compose.dev.yml down -v
```

## 📋 Diferença Entre os Arquivos

### docker-compose.dev.yml (USAR AGORA)
- **5 serviços**: PostgreSQL, Redis, RabbitMQ, MinIO, MediaMTX
- **Uso**: Desenvolvimento local Sprint 11
- **Backend/Streaming**: Rodam via Poetry localmente

### docker-compose.yml (NÃO USAR AGORA)
- **15 serviços**: Tudo acima + Backend, Streaming, Nginx, HAProxy, Kong, Prometheus, Grafana, ELK
- **Uso**: Produção ou testes completos
- **Backend/Streaming**: Rodam em containers Docker

## 🚀 Sequência Correta Sprint 11

```bash
# 1. Limpar tudo
docker-compose -f docker-compose.dev.yml down -v

# 2. Iniciar infraestrutura
scripts\start-infra.bat

# 3. Aguardar 30s
timeout /t 30

# 4. Verificar status
docker-compose -f docker-compose.dev.yml ps

# 5. Instalar dependências Python
poetry install

# 6. Inicializar MinIO
poetry run python scripts\init_minio.py

# 7. Aplicar migrations
poetry run python manage.py migrate

# 8. Rodar Django
poetry run python manage.py runserver

# 9. Rodar FastAPI (outro terminal)
cd src/streaming
poetry run uvicorn infrastructure.web.main:app --reload --port 8001
```

## 🎯 Resultado Esperado

Após `scripts\start-infra.bat`:

```
NAME                      IMAGE                           STATUS
gtvision-postgres-dev     postgres:15-alpine              Up (healthy)
gtvision-redis-dev        redis:7-alpine                  Up (healthy)
gtvision-rabbitmq-dev     rabbitmq:3-management-alpine    Up (healthy)
gtvision-minio-dev        minio/minio:latest              Up (healthy)
gtvision-mediamtx-dev     bluenviron/mediamtx:latest      Up
```

**Total: 5 containers** (não 15!)

## 📝 Scripts Criados

- ✅ `scripts/start-infra.bat` - Inicia infraestrutura
- ✅ `scripts/stop-infra.bat` - Para infraestrutura
- ✅ `scripts/cleanup.bat` - Limpa tudo
- ✅ `scripts/sprint11-setup.bat` - Setup completo

## ⚠️ Lembre-se

**SEMPRE adicione `-f docker-compose.dev.yml`** quando usar docker-compose para Sprint 11!

---

**Execute agora**:
```bash
scripts\start-infra.bat
```
