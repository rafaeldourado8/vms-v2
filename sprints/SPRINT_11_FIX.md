# Sprint 11 - Correção Aplicada

## ❌ Problema Encontrado

Erro ao buildar imagens Docker:
```
The option "--no-dev" does not exist
```

## ✅ Solução Aplicada

### 1. Dockerfile Corrigido
**Arquivo**: `docker/backend/Dockerfile`

**Antes**:
```dockerfile
poetry install --no-dev --no-interaction --no-ansi
```

**Depois**:
```dockerfile
poetry install --only main --no-interaction --no-ansi
```

**Motivo**: Poetry 2.2+ não aceita mais `--no-dev`, use `--only main` ou `--without dev`

### 2. Script de Setup Atualizado
**Arquivo**: `scripts/setup.bat`

**Mudança**: Removido build de imagens Docker (não necessário para desenvolvimento local)

## 🚀 Como Continuar

### Opção 1: Desenvolvimento Local (RECOMENDADO)
```bash
# 1. Iniciar apenas infraestrutura
scripts\sprint11-setup.bat

# 2. Instalar dependências
poetry install

# 3. Aplicar migrations
poetry run python manage.py migrate

# 4. Rodar Django localmente
poetry run python manage.py runserver

# 5. Rodar FastAPI localmente (outro terminal)
cd src/streaming
poetry run uvicorn infrastructure.web.main:app --reload --port 8001
```

### Opção 2: Docker Completo (Produção)
```bash
# 1. Build das imagens (agora vai funcionar)
docker-compose build

# 2. Subir tudo
docker-compose up -d
```

## 📝 Arquivos Corrigidos

- ✅ `docker/backend/Dockerfile` - Flag Poetry corrigida
- ✅ `scripts/setup.bat` - Removido build Docker

## 🎯 Próximo Passo

Execute o setup da Sprint 11:
```bash
scripts\sprint11-setup.bat
```

Isso vai:
1. Iniciar PostgreSQL, Redis, RabbitMQ, MinIO, MediaMTX
2. Criar buckets no MinIO
3. Validar conexões

Depois:
```bash
poetry install
poetry run python manage.py migrate
```

---

**Status**: ✅ Correção aplicada  
**Próxima ação**: `scripts\sprint11-setup.bat`
