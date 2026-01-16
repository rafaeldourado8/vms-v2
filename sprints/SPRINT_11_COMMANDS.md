# Sprint 11 - Comandos Corretos

## ❌ Problema Atual

Você executou comandos do docker-compose errado e containers antigos estão rodando.

**Containers errados rodando**:
- `gtvision-streaming-test` (do docker-compose.test.yml)
- MediaMTX não iniciou

## ✅ Solução

### 1. Limpar Tudo

```bash
# Execute o script de cleanup
scripts\cleanup.bat
```

OU manualmente:

```bash
# Parar TODOS os containers
docker-compose -f docker-compose.yml down -v
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.test.yml down -v

# Remover containers órfãos
docker container prune -f
```

### 2. Iniciar Corretamente

```bash
# Execute o setup da Sprint 11
scripts\sprint11-setup.bat
```

Isso vai iniciar **APENAS** os 5 serviços de infraestrutura:
- ✅ PostgreSQL (gtvision-postgres-dev)
- ✅ Redis (gtvision-redis-dev)
- ✅ RabbitMQ (gtvision-rabbitmq-dev)
- ✅ MinIO (gtvision-minio-dev)
- ✅ MediaMTX (gtvision-mediamtx-dev)

### 3. Validar

```bash
# Ver containers rodando
docker-compose -f docker-compose.dev.yml ps

# Deve mostrar 5 containers com status "Up" e "healthy"
```

## 📋 Comandos Corretos

### Para Sprint 11 (Desenvolvimento Local)

```bash
# Iniciar infraestrutura
scripts\sprint11-setup.bat

# Ver status
docker-compose -f docker-compose.dev.yml ps

# Ver logs
docker-compose -f docker-compose.dev.yml logs -f

# Parar tudo
docker-compose -f docker-compose.dev.yml down

# Parar e limpar volumes
docker-compose -f docker-compose.dev.yml down -v
```

### Para Produção (Futuro)

```bash
# Iniciar tudo (incluindo backend e streaming)
docker-compose up -d

# Ver status
docker-compose ps

# Parar tudo
docker-compose down
```

## 🎯 Resultado Esperado

Após executar `scripts\sprint11-setup.bat`, você deve ver:

```
NAME                      IMAGE                           STATUS
gtvision-postgres-dev     postgres:15-alpine              Up (healthy)
gtvision-redis-dev        redis:7-alpine                  Up (healthy)
gtvision-rabbitmq-dev     rabbitmq:3-management-alpine    Up (healthy)
gtvision-minio-dev        minio/minio:latest              Up (healthy)
gtvision-mediamtx-dev     bluenviron/mediamtx:latest      Up
```

**Total**: 5 containers

## 🚀 Próximos Passos

Após validar que os 5 containers estão rodando:

```bash
# 1. Instalar dependências
poetry install

# 2. Aplicar migrations
poetry run python manage.py migrate

# 3. Inicializar MinIO (criar buckets)
poetry run python scripts\init_minio.py

# 4. Rodar Django
poetry run python manage.py runserver

# 5. Rodar FastAPI (outro terminal)
cd src/streaming
poetry run uvicorn infrastructure.web.main:app --reload --port 8001
```

## ⚠️ Importante

**SEMPRE use `docker-compose.dev.yml` para desenvolvimento local**:
- ✅ `docker-compose -f docker-compose.dev.yml up -d`
- ❌ `docker-compose up -d` (usa docker-compose.yml - produção)

---

**Execute agora**:
```bash
scripts\cleanup.bat
scripts\sprint11-setup.bat
```
