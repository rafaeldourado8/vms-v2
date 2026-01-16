# 🚀 GT-Vision VMS - Guia de Desenvolvimento

## 🎯 Estratégia de Desenvolvimento

**Infraestrutura no Docker** + **Aplicações localmente via Poetry**

### Vantagens:
✅ Hot reload instantâneo (Django + FastAPI)  
✅ Debug fácil (breakpoints, logs)  
✅ Testes rápidos  
✅ Sem rebuild de imagens  
✅ Infraestrutura isolada  

---

## 📋 Pré-requisitos

1. **Docker Desktop** instalado e rodando
2. **Python 3.11+** instalado
3. **Poetry** instalado: `pip install poetry`
4. Arquivo `.env` configurado (já criado)

---

## 🚀 Quick Start

### 1. Iniciar Infraestrutura (Docker)

```bash
scripts\start-dev.bat
```

Isso vai:
- Iniciar PostgreSQL, Redis, RabbitMQ, MinIO, MediaMTX
- Iniciar Prometheus, Grafana, Elasticsearch, Logstash, Kibana
- Criar buckets no MinIO
- Aplicar migrations no PostgreSQL

### 2. Instalar Dependências (Primeira vez)

```bash
poetry install
```

### 3. Iniciar Django (Terminal 1)

```bash
poetry run python manage.py runserver
```

Acesse: http://localhost:8000/admin

### 4. Iniciar FastAPI (Terminal 2)

```bash
cd src/streaming
poetry run uvicorn infrastructure.web.main:app --reload --port 8001
```

Acesse: http://localhost:8001/docs

---

## 🌐 Serviços Disponíveis

### Aplicações (Local)
- **Django Admin**: http://localhost:8000/admin
- **Django API**: http://localhost:8000/api
- **Streaming API**: http://localhost:8001/docs
- **Streaming Metrics**: http://localhost:8001/metrics

### Infraestrutura (Docker)
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **RabbitMQ Management**: http://localhost:15672 (gtvision/gtvision_password)
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin)
- **MediaMTX RTSP**: rtsp://localhost:8554
- **MediaMTX HLS**: http://localhost:8888

### Observabilidade (Docker)
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **Elasticsearch**: http://localhost:9200
- **Kibana**: http://localhost:5601

---

## 🔧 Comandos Úteis

### Infraestrutura

```bash
# Ver logs da infraestrutura
docker-compose -f docker-compose.dev.yml logs -f

# Ver logs de um serviço específico
docker-compose -f docker-compose.dev.yml logs -f postgres
docker-compose -f docker-compose.dev.yml logs -f rabbitmq

# Reiniciar um serviço
docker-compose -f docker-compose.dev.yml restart postgres

# Parar infraestrutura
docker-compose -f docker-compose.dev.yml down

# Parar e limpar volumes (CUIDADO!)
docker-compose -f docker-compose.dev.yml down -v
```

### Django

```bash
# Criar migrations
poetry run python manage.py makemigrations

# Aplicar migrations
poetry run python manage.py migrate

# Criar superuser
poetry run python manage.py createsuperuser

# Django shell
poetry run python manage.py shell

# Coletar static files
poetry run python manage.py collectstatic
```

### FastAPI

```bash
# Iniciar com reload
cd src/streaming
poetry run uvicorn infrastructure.web.main:app --reload --port 8001

# Iniciar com debug
cd src/streaming
poetry run uvicorn infrastructure.web.main:app --reload --port 8001 --log-level debug
```

### Testes

```bash
# Todos os testes
poetry run pytest

# Testes unitários
poetry run pytest -m unit

# Testes de integração
poetry run pytest -m integration

# Com cobertura
poetry run pytest --cov=src --cov-report=html

# Testes específicos
poetry run pytest src/streaming/tests/
poetry run pytest src/admin/tests/
```

### Code Quality

```bash
# Formatação
poetry run black src/
poetry run isort src/

# Linting
poetry run flake8 src/

# Type checking
poetry run mypy src/

# Tudo de uma vez
scripts\lint.bat
```

---

## 🐛 Troubleshooting

### Problema: Poetry não encontrado
```bash
pip install poetry
```

### Problema: Dependências não instaladas
```bash
poetry install
```

### Problema: Porta 8000 já em uso
```bash
# Ver processo
netstat -ano | findstr :8000

# Matar processo
taskkill /PID <PID> /F

# Ou usar outra porta
poetry run python manage.py runserver 8002
```

### Problema: PostgreSQL não conecta
```bash
# Verificar se está rodando
docker-compose -f docker-compose.dev.yml ps postgres

# Ver logs
docker-compose -f docker-compose.dev.yml logs postgres

# Reiniciar
docker-compose -f docker-compose.dev.yml restart postgres
```

### Problema: Migrations não aplicadas
```bash
poetry run python manage.py migrate
```

### Problema: MinIO buckets não criados
```bash
poetry run python scripts\init_minio.py
```

---

## 🔄 Workflow de Desenvolvimento

### 1. Iniciar ambiente
```bash
scripts\start-dev.bat
```

### 2. Abrir 2 terminais

**Terminal 1 - Django**:
```bash
poetry run python manage.py runserver
```

**Terminal 2 - FastAPI**:
```bash
cd src/streaming
poetry run uvicorn infrastructure.web.main:app --reload --port 8001
```

### 3. Fazer alterações no código
- Hot reload automático
- Veja mudanças instantaneamente

### 4. Executar testes
```bash
poetry run pytest
```

### 5. Commit
```bash
git add .
git commit -m "feat: nova funcionalidade"
```

### 6. Parar ambiente
```bash
# Ctrl+C nos terminais Django/FastAPI
docker-compose -f docker-compose.dev.yml down
```

---

## 📊 Monitoramento em Desenvolvimento

### Ver métricas
- **Prometheus**: http://localhost:9090/targets
- **Grafana**: http://localhost:3000/dashboards

### Ver logs
- **Kibana**: http://localhost:5601/app/discover
- **Console**: Logs aparecem nos terminais Django/FastAPI

### Ver filas
- **RabbitMQ**: http://localhost:15672/#/queues

---

## ✅ Checklist de Setup

- [ ] Docker Desktop rodando
- [ ] Poetry instalado (`poetry --version`)
- [ ] Arquivo `.env` existe
- [ ] Infraestrutura iniciada (`scripts\start-dev.bat`)
- [ ] Dependências instaladas (`poetry install`)
- [ ] Migrations aplicadas (`poetry run python manage.py migrate`)
- [ ] Django rodando (Terminal 1)
- [ ] FastAPI rodando (Terminal 2)
- [ ] Django acessível (http://localhost:8000)
- [ ] FastAPI acessível (http://localhost:8001/docs)

---

## 🎯 Próximos Passos

1. **Criar superuser**:
```bash
poetry run python manage.py createsuperuser
```

2. **Acessar admin**:
http://localhost:8000/admin

3. **Testar API**:
http://localhost:8001/docs

4. **Ver métricas**:
http://localhost:9090

5. **Ver logs**:
http://localhost:5601

---

## 🚀 Pronto para Desenvolver!

Ambiente configurado. Agora você pode:
- Editar código com hot reload
- Debugar com breakpoints
- Executar testes rapidamente
- Ver logs em tempo real
- Monitorar métricas
