# Docker Build Troubleshooting

## Correções Aplicadas

### 1. Backend (Django)
- ❌ Removido Poetry (complexo)
- ✅ Instalação direta via pip
- ✅ Apenas dependências essenciais

### 2. Streaming (FastAPI)
- ❌ Removido pyproject.toml
- ✅ Instalação direta via pip
- ✅ PYTHONPATH configurado

### 3. Detection (FastAPI)
- ✅ Versões fixas de dependências
- ✅ PYTHONPATH configurado
- ✅ Estrutura simplificada

### 4. Frontend (React + Vite)
- ✅ Fallback npm install se npm ci falhar
- ✅ Build sem TypeScript check
- ✅ .env criado automaticamente
- ✅ nginx.conf configurado

## Como Fazer Build

### Opção 1: Build Individual (Recomendado)
```bash
# Testar cada serviço separadamente
docker-compose build detection
docker-compose build backend
docker-compose build streaming
docker-compose build frontend
```

### Opção 2: Build Automatizado
```bash
scripts\docker-build.bat
```

### Opção 3: Build Completo
```bash
docker-compose build
```

## Iniciar Serviços

### Apenas Infraestrutura
```bash
docker-compose up -d postgres redis rabbitmq minio mediamtx
```

### Adicionar APIs
```bash
docker-compose up -d detection backend streaming
```

### Adicionar Frontend
```bash
docker-compose up -d frontend nginx haproxy
```

### Tudo de Uma Vez
```bash
docker-compose up -d
```

## Verificar Status

```bash
# Ver logs
docker-compose logs -f [service_name]

# Ver status
docker-compose ps

# Verificar saúde
docker-compose ps | findstr healthy
```

## Problemas Comuns

### Build Falha
```bash
# Limpar cache
docker-compose build --no-cache [service_name]

# Remover imagens antigas
docker system prune -a
```

### Porta em Uso
```bash
# Ver portas em uso
netstat -ano | findstr :[PORT]

# Parar todos os containers
docker-compose down
```

### Frontend não Carrega
```bash
# Verificar se .env existe
dir frontend\.env

# Recriar .env
copy frontend\.env.example frontend\.env
```

## Ordem de Inicialização

1. **Infraestrutura** (postgres, redis, rabbitmq, minio, mediamtx)
2. **Detection API** (sem dependências)
3. **Backend** (depende de infra)
4. **Streaming** (depende de infra + mediamtx)
5. **Frontend** (depende de APIs)
6. **Nginx** (depende de backend)
7. **HAProxy** (depende de tudo)
8. **Kong** (depende de APIs)

## Portas Utilizadas

- 80: HAProxy
- 5173: Frontend (dev)
- 8000: Backend (Django)
- 8001: Streaming (FastAPI)
- 8002: Detection (FastAPI)
- 8080: Nginx
- 8443: Kong Proxy
- 8444: Kong Admin
- 8404: HAProxy Stats
- 5432: PostgreSQL
- 6379: Redis
- 5672: RabbitMQ
- 15672: RabbitMQ Management
- 9000: MinIO API
- 9001: MinIO Console
- 8554: MediaMTX RTSP
- 8889: MediaMTX HLS
- 3000: Grafana
- 9090: Prometheus
- 5601: Kibana
- 9200: Elasticsearch
