# GT-Vision VMS - Arquitetura Final

```excalidraw
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "type": "rectangle",
      "id": "client",
      "x": 400,
      "y": 50,
      "width": 200,
      "height": 80,
      "fillStyle": "solid",
      "strokeColor": "#1e88e5",
      "backgroundColor": "#bbdefb",
      "label": "Cliente\n(Browser/Mobile)"
    },
    {
      "type": "arrow",
      "id": "client-haproxy",
      "x": 500,
      "y": 130,
      "endX": 500,
      "endY": 200,
      "strokeColor": "#1e88e5"
    },
    {
      "type": "rectangle",
      "id": "haproxy",
      "x": 400,
      "y": 200,
      "width": 200,
      "height": 80,
      "fillStyle": "solid",
      "strokeColor": "#f57c00",
      "backgroundColor": "#ffe0b2",
      "label": "HAProxy\n(Load Balancer)\n:8404"
    },
    {
      "type": "arrow",
      "id": "haproxy-kong",
      "x": 500,
      "y": 280,
      "endX": 500,
      "endY": 350,
      "strokeColor": "#f57c00"
    },
    {
      "type": "rectangle",
      "id": "kong",
      "x": 400,
      "y": 350,
      "width": 200,
      "height": 80,
      "fillStyle": "solid",
      "strokeColor": "#7b1fa2",
      "backgroundColor": "#e1bee7",
      "label": "Kong Gateway\n(API Gateway)\n:8000"
    },
    {
      "type": "arrow",
      "id": "kong-django",
      "x": 350,
      "y": 430,
      "endX": 250,
      "endY": 500,
      "strokeColor": "#388e3c"
    },
    {
      "type": "arrow",
      "id": "kong-fastapi",
      "x": 650,
      "y": 430,
      "endX": 750,
      "endY": 500,
      "strokeColor": "#00897b"
    },
    {
      "type": "rectangle",
      "id": "django",
      "x": 100,
      "y": 500,
      "width": 300,
      "height": 200,
      "fillStyle": "solid",
      "strokeColor": "#388e3c",
      "backgroundColor": "#c8e6c9",
      "label": "Django 5.0\n:8000\n\n• Admin Context\n• Cidades Context\n• REST API (DRF)\n• JWT Auth"
    },
    {
      "type": "rectangle",
      "id": "fastapi",
      "x": 600,
      "y": 500,
      "width": 300,
      "height": 200,
      "fillStyle": "solid",
      "strokeColor": "#00897b",
      "backgroundColor": "#b2dfdb",
      "label": "FastAPI\n:8001\n\n• Streaming Context\n• AI Context\n• WebSocket\n• Async I/O"
    },
    {
      "type": "rectangle",
      "id": "postgres",
      "x": 100,
      "y": 800,
      "width": 180,
      "height": 100,
      "fillStyle": "solid",
      "strokeColor": "#0277bd",
      "backgroundColor": "#b3e5fc",
      "label": "PostgreSQL 15\n:5432\n\nDatabase"
    },
    {
      "type": "rectangle",
      "id": "redis",
      "x": 320,
      "y": 800,
      "width": 180,
      "height": 100,
      "fillStyle": "solid",
      "strokeColor": "#c62828",
      "backgroundColor": "#ffcdd2",
      "label": "Redis 7\n:6379\n\nCache"
    },
    {
      "type": "rectangle",
      "id": "rabbitmq",
      "x": 540,
      "y": 800,
      "width": 180,
      "height": 100,
      "fillStyle": "solid",
      "strokeColor": "#ef6c00",
      "backgroundColor": "#ffe0b2",
      "label": "RabbitMQ 3\n:5672\n\nMessage Broker"
    },
    {
      "type": "rectangle",
      "id": "minio",
      "x": 760,
      "y": 800,
      "width": 180,
      "height": 100,
      "fillStyle": "solid",
      "strokeColor": "#6a1b9a",
      "backgroundColor": "#e1bee7",
      "label": "MinIO\n:9000\n\nS3 Storage"
    },
    {
      "type": "rectangle",
      "id": "mediamtx",
      "x": 980,
      "y": 500,
      "width": 200,
      "height": 200,
      "fillStyle": "solid",
      "strokeColor": "#d32f2f",
      "backgroundColor": "#ffcdd2",
      "label": "MediaMTX\n\nRTSP :8554\nRTMP :1935\nHLS :8888\nWebRTC :8889"
    },
    {
      "type": "rectangle",
      "id": "prometheus",
      "x": 100,
      "y": 1000,
      "width": 150,
      "height": 80,
      "fillStyle": "solid",
      "strokeColor": "#e65100",
      "backgroundColor": "#ffe0b2",
      "label": "Prometheus\n:9090"
    },
    {
      "type": "rectangle",
      "id": "grafana",
      "x": 280,
      "y": 1000,
      "width": 150,
      "height": 80,
      "fillStyle": "solid",
      "strokeColor": "#f57c00",
      "backgroundColor": "#ffe0b2",
      "label": "Grafana\n:3000"
    },
    {
      "type": "rectangle",
      "id": "elasticsearch",
      "x": 460,
      "y": 1000,
      "width": 150,
      "height": 80,
      "fillStyle": "solid",
      "strokeColor": "#00897b",
      "backgroundColor": "#b2dfdb",
      "label": "Elasticsearch\n:9200"
    },
    {
      "type": "rectangle",
      "id": "logstash",
      "x": 640,
      "y": 1000,
      "width": 150,
      "height": 80,
      "fillStyle": "solid",
      "strokeColor": "#00897b",
      "backgroundColor": "#b2dfdb",
      "label": "Logstash\n:5000"
    },
    {
      "type": "rectangle",
      "id": "kibana",
      "x": 820,
      "y": 1000,
      "width": 150,
      "height": 80,
      "fillStyle": "solid",
      "strokeColor": "#00897b",
      "backgroundColor": "#b2dfdb",
      "label": "Kibana\n:5601"
    },
    {
      "type": "arrow",
      "id": "django-postgres",
      "x": 190,
      "y": 700,
      "endX": 190,
      "endY": 800,
      "strokeColor": "#0277bd",
      "label": "SQL"
    },
    {
      "type": "arrow",
      "id": "django-redis",
      "x": 300,
      "y": 700,
      "endX": 380,
      "endY": 800,
      "strokeColor": "#c62828",
      "label": "Cache"
    },
    {
      "type": "arrow",
      "id": "django-rabbitmq",
      "x": 400,
      "y": 700,
      "endX": 580,
      "endY": 800,
      "strokeColor": "#ef6c00",
      "label": "Events"
    },
    {
      "type": "arrow",
      "id": "fastapi-postgres",
      "x": 700,
      "y": 700,
      "endX": 280,
      "endY": 850,
      "strokeColor": "#0277bd",
      "label": "SQL"
    },
    {
      "type": "arrow",
      "id": "fastapi-redis",
      "x": 650,
      "y": 700,
      "endX": 500,
      "endY": 850,
      "strokeColor": "#c62828",
      "label": "Cache"
    },
    {
      "type": "arrow",
      "id": "fastapi-rabbitmq",
      "x": 700,
      "y": 700,
      "endX": 630,
      "endY": 800,
      "strokeColor": "#ef6c00",
      "label": "Events"
    },
    {
      "type": "arrow",
      "id": "fastapi-minio",
      "x": 800,
      "y": 700,
      "endX": 850,
      "endY": 800,
      "strokeColor": "#6a1b9a",
      "label": "S3"
    },
    {
      "type": "arrow",
      "id": "fastapi-mediamtx",
      "x": 900,
      "y": 600,
      "endX": 980,
      "endY": 600,
      "strokeColor": "#d32f2f",
      "label": "RTSP/HLS"
    },
    {
      "type": "text",
      "id": "title",
      "x": 300,
      "y": 10,
      "text": "GT-Vision VMS - Arquitetura Final (Sprint 11)",
      "fontSize": 24,
      "fontFamily": 1,
      "textAlign": "center"
    },
    {
      "type": "rectangle",
      "id": "legend",
      "x": 1050,
      "y": 50,
      "width": 250,
      "height": 400,
      "fillStyle": "solid",
      "strokeColor": "#424242",
      "backgroundColor": "#f5f5f5",
      "label": "LEGENDA\n\n🔵 Cliente Layer\n🟠 Proxy Layer\n🟣 Gateway Layer\n🟢 Backend Layer\n🔴 Streaming Layer\n🔵 Data Layer\n🟡 Observability\n\nFluxos:\n→ HTTP/REST\n⇢ WebSocket\n⇝ RTSP/HLS\n⤏ Events (RabbitMQ)\n⤑ SQL/Cache"
    }
  ]
}
```

## Descrição da Arquitetura

### Camadas

#### 1. Cliente Layer
- **Browser/Mobile**: Interface do usuário
- Acesso via HTTP/HTTPS

#### 2. Proxy Layer
- **HAProxy** (:8404): Load balancer, SSL termination, rate limiting
- Distribui tráfego entre instâncias

#### 3. Gateway Layer
- **Kong Gateway** (:8000): API Gateway, autenticação, rate limiting
- Roteamento inteligente para backends

#### 4. Backend Layer

**Django (Admin + Cidades)**
- Porta: 8000
- Contexts: Admin, Cidades
- Tech: Django 5.0 + DRF
- Auth: JWT
- Pattern: DDD

**FastAPI (Streaming + AI)**
- Porta: 8001
- Contexts: Streaming, AI
- Tech: FastAPI + Async
- WebSocket: Real-time
- Pattern: DDD

#### 5. Streaming Layer
- **MediaMTX**: Servidor de streaming
  - RTSP: 8554 (ingestão)
  - RTMP: 1935 (alternativo)
  - HLS: 8888 (playback)
  - WebRTC: 8889 (baixa latência)

#### 6. Data Layer

**PostgreSQL 15** (:5432)
- Database principal
- Dados transacionais
- Metadados

**Redis 7** (:6379)
- Cache distribuído
- Session storage
- Rate limiting

**RabbitMQ 3** (:5672)
- Message broker
- Eventos de domínio
- Comunicação assíncrona

**MinIO** (:9000)
- S3-compatible storage
- Vídeos gravados
- Imagens LPR
- Clips exportados

#### 7. Observability Layer

**Métricas**
- Prometheus (:9090): Coleta métricas
- Grafana (:3000): Dashboards

**Logs**
- Elasticsearch (:9200): Armazenamento
- Logstash (:5000): Processamento
- Kibana (:5601): Visualização

### Fluxos de Dados

#### Fluxo de Autenticação
```
Cliente → HAProxy → Kong → Django Admin → PostgreSQL
                                        → Redis (cache)
```

#### Fluxo de Streaming
```
Câmera → MediaMTX (RTSP) → FastAPI → MinIO (gravação)
                                   → RabbitMQ (eventos)
Cliente ← MediaMTX (HLS) ← FastAPI
```

#### Fluxo de Eventos LPR
```
LPR System → FastAPI AI → PostgreSQL (metadados)
                        → MinIO (imagens)
                        → RabbitMQ (notificações)
```

#### Fluxo de Observabilidade
```
Todos Serviços → Prometheus (métricas)
               → Logstash → Elasticsearch → Kibana (logs)
```

### Comunicação Entre Contexts

#### Síncrona (REST)
- Admin ↔ Cidades: Validação de usuários
- Cidades ↔ Streaming: Validação de câmeras
- Streaming ↔ AI: Consulta de eventos

#### Assíncrona (RabbitMQ)
- Cidades → Streaming: `camera.created`, `camera.deleted`
- Streaming → AI: `recording.started`, `recording.stopped`
- AI → Cidades: `lpr.detected`, `alert.triggered`

### Escalabilidade

#### Horizontal
- Django: N instâncias (stateless)
- FastAPI: N instâncias (stateless)
- HAProxy: Load balancing
- Redis: Cluster mode
- RabbitMQ: Cluster mode

#### Vertical
- PostgreSQL: Connection pooling
- MediaMTX: Multi-stream support
- MinIO: Distributed mode

### Segurança

#### Camadas de Proteção
1. HAProxy: Rate limiting, DDoS protection
2. Kong: JWT validation, API key
3. Backend: RBAC, input validation
4. Database: Prepared statements, encryption

#### Compliance
- OWASP Top 10 ✅
- LGPD ✅
- Auditoria completa ✅

### Performance

#### Targets
- Latência API: < 100ms (p95)
- Latência Streaming: < 2s (HLS)
- Throughput: 1000 req/s
- Câmeras simultâneas: 100+

#### Otimizações
- Cache Redis (TTL inteligente)
- Connection pooling
- Async I/O (FastAPI)
- CDN para HLS (futuro)

### Deployment

#### Desenvolvimento
```bash
docker-compose -f docker-compose.dev.yml up -d
poetry run python manage.py runserver
poetry run uvicorn infrastructure.web.main:app --reload --port 8001
```

#### Produção
```bash
docker-compose up -d
# ou
terraform apply (AWS)
```

### Monitoramento

#### Dashboards Grafana
- System Overview
- API Performance
- Streaming Health
- Database Metrics
- Business KPIs

#### Alertas
- CPU > 80%
- Memory > 85%
- Disk > 90%
- API errors > 1%
- Streaming failures

### Backup & Recovery

#### Dados
- PostgreSQL: Daily backup (7 dias)
- MinIO: Replicação S3
- Redis: RDB snapshots

#### Disaster Recovery
- RTO: < 4 horas
- RPO: < 1 hora
- Backup offsite (S3)
