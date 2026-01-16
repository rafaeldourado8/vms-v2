# 🚀 GT-Vision VMS - Quick Start (Docker)

## ✅ Pré-requisitos

- Docker Desktop instalado e rodando
- Arquivo `.env` configurado (já criado)

---

## 🎯 Opção 1: Comando Único (RECOMENDADO)

```bash
# Iniciar stack completa
scripts\start-full-stack.bat
```

Isso vai:
1. Parar containers antigos
2. Construir imagens
3. Iniciar toda a stack
4. Aguardar serviços iniciarem

---

## 🎯 Opção 2: Comandos Manuais

### 1. Construir imagens
```bash
docker-compose build
```

### 2. Iniciar stack
```bash
docker-compose up -d
```

### 3. Ver logs
```bash
docker-compose logs -f
```

### 4. Verificar status
```bash
docker-compose ps
```

---

## 🌐 Serviços Disponíveis

### Aplicações
- **Django Admin**: http://localhost:8000/admin
- **Streaming API**: http://localhost:8001/docs
- **Nginx**: http://localhost:8080

### Infraestrutura
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **RabbitMQ Management**: http://localhost:15672 (gtvision/gtvision_password)
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin)
- **MediaMTX RTSP**: rtsp://localhost:8554
- **MediaMTX HLS**: http://localhost:8888

### Observabilidade
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **Elasticsearch**: http://localhost:9200
- **Kibana**: http://localhost:5601

### Proxy
- **HAProxy**: http://localhost:80
- **HAProxy Stats**: http://localhost:8404/stats

---

## 🔧 Comandos Úteis

### Ver logs de um serviço específico
```bash
docker-compose logs -f backend
docker-compose logs -f streaming
docker-compose logs -f postgres
```

### Reiniciar um serviço
```bash
docker-compose restart backend
docker-compose restart streaming
```

### Parar stack
```bash
docker-compose down
```

### Parar e limpar volumes (CUIDADO!)
```bash
docker-compose down -v
```

### Executar comando dentro de um container
```bash
# Django shell
docker-compose exec backend python manage.py shell

# Migrations
docker-compose exec backend python manage.py migrate

# Criar superuser
docker-compose exec backend python manage.py createsuperuser

# PostgreSQL
docker-compose exec postgres psql -U gtvision -d gtvision
```

---

## 🧪 Testar Stack

### 1. Health Check
```bash
# Backend
curl http://localhost:8000/health

# Streaming
curl http://localhost:8001/health

# Prometheus
curl http://localhost:9090/-/healthy

# Elasticsearch
curl http://localhost:9200/_cluster/health
```

### 2. Criar Superuser Django
```bash
docker-compose exec backend python manage.py createsuperuser
```

### 3. Acessar Admin
http://localhost:8000/admin

### 4. Testar Streaming API
http://localhost:8001/docs

---

## 🐛 Troubleshooting

### Problema: Porta já em uso
```bash
# Ver processos usando porta
netstat -ano | findstr :8000

# Matar processo
taskkill /PID <PID> /F
```

### Problema: Container não inicia
```bash
# Ver logs
docker-compose logs <service_name>

# Reiniciar
docker-compose restart <service_name>
```

### Problema: Banco de dados não conecta
```bash
# Verificar se PostgreSQL está rodando
docker-compose ps postgres

# Ver logs
docker-compose logs postgres

# Aguardar 30s após docker-compose up
```

### Problema: Migrations não aplicadas
```bash
# Aplicar migrations manualmente
docker-compose exec backend python manage.py migrate
```

---

## 📊 Monitoramento

### Prometheus Targets
http://localhost:9090/targets

### Grafana Dashboards
http://localhost:3000/dashboards

### Kibana Logs
http://localhost:5601/app/discover

### RabbitMQ Queues
http://localhost:15672/#/queues

---

## 🔄 Workflow de Desenvolvimento

### 1. Iniciar stack
```bash
scripts\start-full-stack.bat
```

### 2. Fazer alterações no código
- Código em `src/` é montado como volume
- Hot reload automático (Django + FastAPI)

### 3. Ver logs em tempo real
```bash
docker-compose logs -f backend streaming
```

### 4. Executar testes
```bash
docker-compose exec backend pytest
docker-compose exec streaming pytest
```

### 5. Parar stack
```bash
docker-compose down
```

---

## ✅ Checklist de Validação

- [ ] Docker Desktop rodando
- [ ] Arquivo `.env` existe
- [ ] `docker-compose build` executado
- [ ] `docker-compose up -d` executado
- [ ] Todos os containers rodando (`docker-compose ps`)
- [ ] Backend acessível (http://localhost:8000/health)
- [ ] Streaming acessível (http://localhost:8001/health)
- [ ] Prometheus acessível (http://localhost:9090)
- [ ] Grafana acessível (http://localhost:3000)
- [ ] Kibana acessível (http://localhost:5601)

---

## 🎉 Pronto!

Stack completa rodando no Docker. Sem necessidade de Poetry local!

**Próximos passos**:
1. Criar superuser: `docker-compose exec backend python manage.py createsuperuser`
2. Acessar admin: http://localhost:8000/admin
3. Testar API: http://localhost:8001/docs
