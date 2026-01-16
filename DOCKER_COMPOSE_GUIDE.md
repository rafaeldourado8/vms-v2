# Docker Compose - Guia Completo

## 🎯 Arquitetura Completa

```
                    ┌─────────────┐
                    │   HAProxy   │ :80
                    │  (Balancer) │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌─────▼─────┐     ┌─────▼─────┐
   │Frontend │       │  Backend  │     │ Streaming │
   │  :5173  │       │   :8000   │     │   :8001   │
   └─────────┘       └───────────┘     └───────────┘
                           │                  │
                     ┌─────▼─────┐     ┌─────▼─────┐
                     │PostgreSQL │     │ Detection │
                     │   :5432   │     │   :8002   │
                     └───────────┘     └───────────┘
                           │
                     ┌─────▼─────┐
                     │  MediaMTX │
                     │   :8889   │
                     └───────────┘
```

## 📋 Serviços

### Infraestrutura
- **PostgreSQL** (5432) - Banco de dados
- **Redis** (6379) - Cache
- **RabbitMQ** (5672, 15672) - Message broker
- **MinIO** (9000, 9001) - Storage S3

### Aplicação
- **Backend** (8000) - Django API
- **Streaming** (8001) - FastAPI Streaming
- **Detection** (8002) - FastAPI Detection
- **Frontend** (5173) - React + Vite

### Streaming
- **MediaMTX** (8889) - HLS Server

### Gateway
- **HAProxy** (80, 8404) - Load balancer
- **Kong** (8443, 8444) - API Gateway

### Observabilidade
- **Prometheus** (9090) - Métricas
- **Grafana** (3000) - Dashboards
- **Elasticsearch** (9200) - Logs
- **Logstash** (5000) - Log processor
- **Kibana** (5601) - Log viewer

## 🚀 Comandos

### Iniciar Tudo

```bash
docker-compose up -d
```

### Iniciar Apenas Infraestrutura

```bash
docker-compose up -d postgres redis rabbitmq minio mediamtx
```

### Iniciar Aplicação

```bash
docker-compose up -d backend streaming detection frontend
```

### Ver Logs

```bash
# Todos
docker-compose logs -f

# Específico
docker-compose logs -f backend
docker-compose logs -f streaming
docker-compose logs -f detection
docker-compose logs -f frontend
```

### Parar Tudo

```bash
docker-compose down
```

### Parar e Limpar Volumes

```bash
docker-compose down -v
```

### Rebuild

```bash
docker-compose build --no-cache
docker-compose up -d
```

### Restart Serviço

```bash
docker-compose restart backend
docker-compose restart streaming
```

## 🔧 Portas

| Serviço | Porta | URL |
|---------|-------|-----|
| HAProxy | 80 | http://localhost |
| HAProxy Stats | 8404 | http://localhost:8404/stats |
| Frontend | 5173 | http://localhost:5173 |
| Backend | 8000 | http://localhost:8000 |
| Streaming | 8001 | http://localhost:8001 |
| Detection | 8002 | http://localhost:8002 |
| MediaMTX HLS | 8889 | http://localhost:8889 |
| PostgreSQL | 5432 | localhost:5432 |
| Redis | 6379 | localhost:6379 |
| RabbitMQ | 5672, 15672 | http://localhost:15672 |
| MinIO | 9000, 9001 | http://localhost:9001 |
| Prometheus | 9090 | http://localhost:9090 |
| Grafana | 3000 | http://localhost:3000 |
| Kibana | 5601 | http://localhost:5601 |
| Kong | 8443, 8444 | https://localhost:8443 |

## 📊 Health Checks

```bash
# Backend
curl http://localhost:8000/health

# Streaming
curl http://localhost:8001/health

# Detection
curl http://localhost:8002/health

# PostgreSQL
docker exec gtvision-postgres pg_isready -U gtvision

# Redis
docker exec gtvision-redis redis-cli ping

# RabbitMQ
curl http://localhost:15672/api/healthchecks/node
```

## 🔐 Credenciais Padrão

### PostgreSQL
- User: `gtvision`
- Password: `gtvision_password`
- Database: `gtvision`

### RabbitMQ
- User: `gtvision`
- Password: `gtvision_password`
- URL: http://localhost:15672

### MinIO
- User: `minioadmin`
- Password: `minioadmin`
- Console: http://localhost:9001

### Grafana
- User: `admin`
- Password: `admin`
- URL: http://localhost:3000

## 🐛 Troubleshooting

### Porta em uso

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Container não inicia

```bash
# Ver logs
docker logs gtvision-backend

# Ver status
docker ps -a

# Rebuild
docker-compose build --no-cache backend
docker-compose up -d backend
```

### Limpar tudo

```bash
docker-compose down -v
docker system prune -a
docker volume prune
```

### Erro de permissão

```bash
# Windows (PowerShell como Admin)
icacls "d:\vms-v2" /grant Everyone:F /T

# Linux/Mac
sudo chown -R $USER:$USER .
```

## 📝 Variáveis de Ambiente

Copie `.env.example` para `.env` e ajuste:

```env
# Database
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=gtvision
POSTGRES_USER=gtvision
POSTGRES_PASSWORD=gtvision_password

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# RabbitMQ
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=gtvision
RABBITMQ_PASSWORD=gtvision_password

# MinIO
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# MediaMTX
MEDIAMTX_HOST=mediamtx
MEDIAMTX_API_PORT=9997
MEDIAMTX_HLS_PORT=8889

# Logstash
LOGSTASH_HOST=logstash
LOGSTASH_PORT=5000
```

## 🚀 Deploy Produção

### 1. Build

```bash
docker-compose -f docker-compose.yml build
```

### 2. Push para Registry

```bash
docker tag gtvision-backend registry.example.com/gtvision-backend
docker push registry.example.com/gtvision-backend
```

### 3. Deploy

```bash
docker-compose -f docker-compose.yml up -d
```

## ✅ Checklist de Inicialização

- [ ] Copiar `.env.example` para `.env`
- [ ] Ajustar variáveis de ambiente
- [ ] Build das imagens: `docker-compose build`
- [ ] Iniciar infraestrutura: `docker-compose up -d postgres redis rabbitmq minio`
- [ ] Aguardar health checks (30s)
- [ ] Iniciar aplicação: `docker-compose up -d backend streaming detection`
- [ ] Iniciar frontend: `docker-compose up -d frontend`
- [ ] Iniciar gateway: `docker-compose up -d haproxy`
- [ ] Verificar health: `curl http://localhost/health`
- [ ] Acessar frontend: http://localhost

---

**Última atualização**: 2025-01-16
