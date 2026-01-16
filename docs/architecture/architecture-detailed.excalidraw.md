# GT-Vision VMS - Arquitetura Detalhada

## Diagrama Excalidraw

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "type": "text",
      "id": "title",
      "x": 400,
      "y": 20,
      "width": 600,
      "height": 40,
      "text": "GT-Vision VMS - Arquitetura Final Sprint 11",
      "fontSize": 28,
      "fontFamily": 1,
      "textAlign": "center",
      "fillStyle": "solid"
    },
    {
      "type": "rectangle",
      "id": "client",
      "x": 500,
      "y": 80,
      "width": 200,
      "height": 100,
      "fillStyle": "solid",
      "strokeColor": "#1e88e5",
      "backgroundColor": "#bbdefb",
      "strokeWidth": 3
    },
    {
      "type": "text",
      "id": "client-text",
      "x": 520,
      "y": 100,
      "width": 160,
      "height": 60,
      "text": "🌐 Cliente\nBrowser/Mobile\nReact/Flutter",
      "fontSize": 16,
      "textAlign": "center"
    },
    {
      "type": "arrow",
      "id": "arrow1",
      "x": 600,
      "y": 180,
      "width": 0,
      "height": 70,
      "strokeColor": "#1e88e5",
      "strokeWidth": 2
    },
    {
      "type": "rectangle",
      "id": "haproxy",
      "x": 500,
      "y": 250,
      "width": 200,
      "height": 120,
      "fillStyle": "solid",
      "strokeColor": "#f57c00",
      "backgroundColor": "#ffe0b2",
      "strokeWidth": 3
    },
    {
      "type": "text",
      "id": "haproxy-text",
      "x": 520,
      "y": 270,
      "width": 160,
      "height": 80,
      "text": "⚖️ HAProxy\n:8404\nLoad Balancer\nSSL Termination\nRate Limiting",
      "fontSize": 14,
      "textAlign": "center"
    },
    {
      "type": "arrow",
      "id": "arrow2",
      "x": 600,
      "y": 370,
      "width": 0,
      "height": 60,
      "strokeColor": "#f57c00",
      "strokeWidth": 2
    },
    {
      "type": "rectangle",
      "id": "kong",
      "x": 500,
      "y": 430,
      "width": 200,
      "height": 120,
      "fillStyle": "solid",
      "strokeColor": "#7b1fa2",
      "backgroundColor": "#e1bee7",
      "strokeWidth": 3
    },
    {
      "type": "text",
      "id": "kong-text",
      "x": 520,
      "y": 450,
      "width": 160,
      "height": 80,
      "text": "🦍 Kong Gateway\n:8000\nAPI Gateway\nJWT Auth\nRouting",
      "fontSize": 14,
      "textAlign": "center"
    },
    {
      "type": "arrow",
      "id": "arrow3",
      "x": 500,
      "y": 490,
      "width": -200,
      "height": 110,
      "strokeColor": "#388e3c",
      "strokeWidth": 2
    },
    {
      "type": "arrow",
      "id": "arrow4",
      "x": 700,
      "y": 490,
      "width": 200,
      "height": 110,
      "strokeColor": "#00897b",
      "strokeWidth": 2
    },
    {
      "type": "rectangle",
      "id": "django",
      "x": 100,
      "y": 600,
      "width": 300,
      "height": 250,
      "fillStyle": "solid",
      "strokeColor": "#388e3c",
      "backgroundColor": "#c8e6c9",
      "strokeWidth": 3
    },
    {
      "type": "text",
      "id": "django-text",
      "x": 120,
      "y": 620,
      "width": 260,
      "height": 210,
      "text": "🐍 Django 5.0\n:8000\n\n📋 Admin Context\n• Users/Roles\n• Audit Logs\n• Multi-tenancy\n\n🏙️ Cidades Context\n• Prefeituras\n• Câmeras\n• Localizações",
      "fontSize": 14,
      "textAlign": "left"
    },
    {
      "type": "rectangle",
      "id": "fastapi",
      "x": 800,
      "y": 600,
      "width": 300,
      "height": 250,
      "fillStyle": "solid",
      "strokeColor": "#00897b",
      "backgroundColor": "#b2dfdb",
      "strokeWidth": 3
    },
    {
      "type": "text",
      "id": "fastapi-text",
      "x": 820,
      "y": 620,
      "width": 260,
      "height": 210,
      "text": "⚡ FastAPI\n:8001\n\n📹 Streaming Context\n• Stream Proxy\n• Recording\n• Snapshots\n\n🤖 AI Context\n• LPR Detection\n• Analytics\n• Alerts",
      "fontSize": 14,
      "textAlign": "left"
    },
    {
      "type": "rectangle",
      "id": "mediamtx",
      "x": 1200,
      "y": 600,
      "width": 250,
      "height": 250,
      "fillStyle": "solid",
      "strokeColor": "#d32f2f",
      "backgroundColor": "#ffcdd2",
      "strokeWidth": 3
    },
    {
      "type": "text",
      "id": "mediamtx-text",
      "x": 1220,
      "y": 620,
      "width": 210,
      "height": 210,
      "text": "📹 MediaMTX\n\nRTSP :8554\n(Ingestão)\n\nRTMP :1935\n(Alternativo)\n\nHLS :8888\n(Playback)\n\nWebRTC :8889\n(Baixa Latência)",
      "fontSize": 14,
      "textAlign": "left"
    },
    {
      "type": "arrow",
      "id": "arrow5",
      "x": 1100,
      "y": 725,
      "width": 100,
      "height": 0,
      "strokeColor": "#d32f2f",
      "strokeWidth": 2
    },
    {
      "type": "rectangle",
      "id": "postgres",
      "x": 100,
      "y": 950,
      "width": 200,
      "height": 120,
      "fillStyle": "solid",
      "strokeColor": "#0277bd",
      "backgroundColor": "#b3e5fc",
      "strokeWidth": 3
    },
    {
      "type": "text",
      "id": "postgres-text",
      "x": 120,
      "y": 970,
      "width": 160,
      "height": 80,
      "text": "🐘 PostgreSQL 15\n:5432\n\nTransactional\nMetadata\nSchemas: 4",
      "fontSize": 14,
      "textAlign": "center"
    },
    {
      "type": "rectangle",
      "id": "redis",
      "x": 350,
      "y": 950,
      "width": 200,
      "height": 120,
      "fillStyle": "solid",
      "strokeColor": "#c62828",
      "backgroundColor": "#ffcdd2",
      "strokeWidth": 3
    },
    {
      "type": "text",
      "id": "redis-text",
      "x": 370,
      "y": 970,
      "width": 160,
      "height": 80,
      "text": "🔴 Redis 7\n:6379\n\nCache\nSessions\nRate Limit",
      "fontSize": 14,
      "textAlign": "center"
    },
    {
      "type": "rectangle",
      "id": "rabbitmq",
      "x": 600,
      "y": 950,
      "width": 200,
      "height": 120,
      "fillStyle": "solid",
      "strokeColor": "#ef6c00",
      "backgroundColor": "#ffe0b2",
      "strokeWidth": 3
    },
    {
      "type": "text",
      "id": "rabbitmq-text",
      "x": 620,
      "y": 970,
      "width": 160,
      "height": 80,
      "text": "🐰 RabbitMQ 3\n:5672/:15672\n\nMessage Broker\nDomain Events\nAsync Tasks",
      "fontSize": 14,
      "textAlign": "center"
    },
    {
      "type": "rectangle",
      "id": "minio",
      "x": 850,
      "y": 950,
      "width": 200,
      "height": 120,
      "fillStyle": "solid",
      "strokeColor": "#6a1b9a",
      "backgroundColor": "#e1bee7",
      "strokeWidth": 3
    },
    {
      "type": "text",
      "id": "minio-text",
      "x": 870,
      "y": 970,
      "width": 160,
      "height": 80,
      "text": "📦 MinIO\n:9000/:9001\n\nS3 Storage\nVideos/Images\nExports",
      "fontSize": 14,
      "textAlign": "center"
    },
    {
      "type": "arrow",
      "id": "django-postgres",
      "x": 200,
      "y": 850,
      "width": 0,
      "height": 100,
      "strokeColor": "#0277bd",
      "strokeWidth": 2
    },
    {
      "type": "arrow",
      "id": "django-redis",
      "x": 300,
      "y": 850,
      "width": 100,
      "height": 100,
      "strokeColor": "#c62828",
      "strokeWidth": 2
    },
    {
      "type": "arrow",
      "id": "django-rabbitmq",
      "x": 400,
      "y": 850,
      "width": 300,
      "height": 100,
      "strokeColor": "#ef6c00",
      "strokeWidth": 2
    },
    {
      "type": "arrow",
      "id": "fastapi-postgres",
      "x": 900,
      "y": 850,
      "width": -700,
      "height": 100,
      "strokeColor": "#0277bd",
      "strokeWidth": 2
    },
    {
      "type": "arrow",
      "id": "fastapi-redis",
      "x": 850,
      "y": 850,
      "width": -400,
      "height": 100,
      "strokeColor": "#c62828",
      "strokeWidth": 2
    },
    {
      "type": "arrow",
      "id": "fastapi-rabbitmq",
      "x": 900,
      "y": 850,
      "width": -200,
      "height": 100,
      "strokeColor": "#ef6c00",
      "strokeWidth": 2
    },
    {
      "type": "arrow",
      "id": "fastapi-minio",
      "x": 950,
      "y": 850,
      "width": 0,
      "height": 100,
      "strokeColor": "#6a1b9a",
      "strokeWidth": 2
    },
    {
      "type": "rectangle",
      "id": "prometheus",
      "x": 100,
      "y": 1150,
      "width": 180,
      "height": 100,
      "fillStyle": "solid",
      "strokeColor": "#e65100",
      "backgroundColor": "#ffe0b2",
      "strokeWidth": 2
    },
    {
      "type": "text",
      "id": "prometheus-text",
      "x": 120,
      "y": 1170,
      "width": 140,
      "height": 60,
      "text": "📊 Prometheus\n:9090\nMetrics",
      "fontSize": 14,
      "textAlign": "center"
    },
    {
      "type": "rectangle",
      "id": "grafana",
      "x": 310,
      "y": 1150,
      "width": 180,
      "height": 100,
      "fillStyle": "solid",
      "strokeColor": "#f57c00",
      "backgroundColor": "#ffe0b2",
      "strokeWidth": 2
    },
    {
      "type": "text",
      "id": "grafana-text",
      "x": 330,
      "y": 1170,
      "width": 140,
      "height": 60,
      "text": "📈 Grafana\n:3000\nDashboards",
      "fontSize": 14,
      "textAlign": "center"
    },
    {
      "type": "rectangle",
      "id": "elasticsearch",
      "x": 520,
      "y": 1150,
      "width": 180,
      "height": 100,
      "fillStyle": "solid",
      "strokeColor": "#00897b",
      "backgroundColor": "#b2dfdb",
      "strokeWidth": 2
    },
    {
      "type": "text",
      "id": "elasticsearch-text",
      "x": 540,
      "y": 1170,
      "width": 140,
      "height": 60,
      "text": "🔍 Elasticsearch\n:9200\nLogs",
      "fontSize": 14,
      "textAlign": "center"
    },
    {
      "type": "rectangle",
      "id": "logstash",
      "x": 730,
      "y": 1150,
      "width": 180,
      "height": 100,
      "fillStyle": "solid",
      "strokeColor": "#00897b",
      "backgroundColor": "#b2dfdb",
      "strokeWidth": 2
    },
    {
      "type": "text",
      "id": "logstash-text",
      "x": 750,
      "y": 1170,
      "width": 140,
      "height": 60,
      "text": "📝 Logstash\n:5000\nProcessing",
      "fontSize": 14,
      "textAlign": "center"
    },
    {
      "type": "rectangle",
      "id": "kibana",
      "x": 940,
      "y": 1150,
      "width": 180,
      "height": 100,
      "fillStyle": "solid",
      "strokeColor": "#00897b",
      "backgroundColor": "#b2dfdb",
      "strokeWidth": 2
    },
    {
      "type": "text",
      "id": "kibana-text",
      "x": 960,
      "y": 1170,
      "width": 140,
      "height": 60,
      "text": "📊 Kibana\n:5601\nVisualization",
      "fontSize": 14,
      "textAlign": "center"
    },
    {
      "type": "rectangle",
      "id": "legend",
      "x": 1200,
      "y": 950,
      "width": 300,
      "height": 300,
      "fillStyle": "solid",
      "strokeColor": "#424242",
      "backgroundColor": "#f5f5f5",
      "strokeWidth": 2
    },
    {
      "type": "text",
      "id": "legend-text",
      "x": 1220,
      "y": 970,
      "width": 260,
      "height": 260,
      "text": "📋 LEGENDA\n\n🔵 Cliente Layer\n🟠 Proxy Layer\n🟣 Gateway Layer\n🟢 Backend Layer\n🔴 Streaming Layer\n🔵 Data Layer\n🟡 Observability\n\nFluxos:\n→ HTTP/REST\n⇢ WebSocket\n⇝ RTSP/HLS\n⤏ Events\n⤑ SQL/Cache",
      "fontSize": 12,
      "textAlign": "left"
    }
  ]
}
```

## Descrição Detalhada dos Componentes

### 🌐 Cliente Layer

**Browser/Mobile**
- Tecnologia: React (Web), Flutter (Mobile)
- Comunicação: HTTPS, WebSocket
- Autenticação: JWT Bearer Token
- Funcionalidades:
  - Dashboard de monitoramento
  - Visualização de streams ao vivo
  - Gestão de câmeras e prefeituras
  - Relatórios e analytics
  - Alertas em tempo real

### ⚖️ HAProxy (:8404)

**Load Balancer de Entrada**
- Função: Balanceamento de carga e SSL termination
- Recursos:
  - SSL/TLS Termination (HTTPS → HTTP)
  - Rate Limiting: 1000 req/min por IP
  - Health Checks: Verifica saúde dos backends
  - Sticky Sessions: Mantém sessão no mesmo backend
  - Stats Dashboard: Monitoramento em tempo real
- Algoritmo: Round Robin com health checks
- Timeout: 30s para conexões HTTP, 3600s para WebSocket

### 🦍 Kong Gateway (:8000)

**API Gateway e Roteamento**
- Função: Gateway centralizado para todas as APIs
- Plugins Ativos:
  - JWT Authentication: Validação de tokens
  - Rate Limiting: 100 req/min por usuário
  - CORS: Configuração de origens permitidas
  - Request Transformation: Modificação de headers
  - Response Transformation: Padronização de respostas
  - Logging: Logs estruturados
- Rotas Configuradas:
  - `/api/admin/*` → Django :8000
  - `/api/cidades/*` → Django :8000
  - `/api/streaming/*` → FastAPI :8001
  - `/api/ai/*` → FastAPI :8001
  - `/ws/*` → FastAPI :8001 (WebSocket)

### 🐍 Django 5.0 (:8000)

**Backend Monolítico - Admin + Cidades**

**Arquitetura DDD:**
- API Layer: Django REST Framework ViewSets
- Application Layer: Use Cases, DTOs, Validators
- Domain Layer: Entities, Value Objects, Domain Services
- Infrastructure Layer: Repositories, ORM, External Services

**Admin Context:**
- Gestão de Usuários e Permissões (RBAC)
- Auditoria de Ações (Audit Logs)
- Configurações do Sistema
- Multi-tenancy (Prefeituras)
- Dashboard Administrativo

**Cidades Context:**
- Cadastro de Prefeituras
- Gestão de Câmeras IP
- Localizações e Zonas Geográficas
- Configurações de Câmeras (RTSP, credenciais)
- Integração com ONVIF

**Tecnologias:**
- Django 5.0 + Django REST Framework
- JWT Authentication (djangorestframework-simplejwt)
- PostgreSQL (Django ORM)
- Redis (django-redis para cache)
- Celery (tarefas assíncronas)

### ⚡ FastAPI (:8001)

**Backend Assíncrono - Streaming + AI**

**Arquitetura DDD Assíncrona:**
- API Layer: FastAPI Routers + WebSocket
- Application Layer: Async Use Cases
- Domain Layer: Aggregates, Domain Events
- Infrastructure Layer: Async Repositories, External APIs

**Streaming Context:**
- Proxy de Streams RTSP → HLS/WebRTC
- Gravação de Vídeos (MP4/HLS)
- Snapshots e Thumbnails
- Gestão de Sessões de Streaming
- Controle PTZ (Pan-Tilt-Zoom)

**AI Context:**
- Detecção de Placas (LPR) com YOLO v8
- Analytics de Tráfego
- Alertas Inteligentes
- Processamento de Frames em Tempo Real
- Reconhecimento de Padrões

**Tecnologias:**
- FastAPI + Uvicorn
- WebSocket para real-time
- Pydantic para validação
- SQLAlchemy Async
- OpenCV + YOLO v8
- TensorFlow/PyTorch

### 📹 MediaMTX

**Servidor de Streaming Multi-Protocolo**

**Protocolos Suportados:**

**RTSP (:8554) - Ingestão**
- Recebe streams de câmeras IP
- Suporta autenticação
- Transcodificação automática

**RTMP (:1935) - Alternativo**
- Protocolo alternativo para ingestão
- Compatibilidade com encoders

**HLS (:8888) - Playback**
- Streaming para browsers
- Latência: 2-3 segundos
- Adaptive bitrate

**WebRTC (:8889) - Baixa Latência**
- Latência ultra-baixa (<1s)
- P2P quando possível
- Ideal para monitoramento em tempo real

**Recursos:**
- Recording em MP4/HLS
- Authentication via HTTP hooks
- Metrics para Prometheus
- On-demand streaming

### 🐘 PostgreSQL 15 (:5432)

**Database Relacional Principal**

**Schemas:**
- `admin`: Users, Roles, Permissions, Audit Logs
- `cidades`: Prefeituras, Cameras, Locations, Zones
- `streaming`: Streams, Recordings, Snapshots
- `ai`: Detections, Plates, Analytics, Alerts

**Recursos:**
- JSONB para metadados flexíveis
- Full-text search para logs
- Particionamento por data (recordings, detections)
- Índices otimizados
- Connection pooling (PgBouncer)

**Backup:**
- Daily automated backups
- Point-in-time recovery
- Retenção: 30 dias

### 🔴 Redis 7 (:6379)

**Cache Distribuído e Session Store**

**Uso:**
- Cache de Queries: TTL 5 minutos
- Session Storage: JWT blacklist
- Rate Limiting: Contadores por IP/usuário
- Real-time Stream Status: Estado dos streams
- Pub/Sub: Notificações em tempo real

**Configuração:**
- Persistência: RDB (snapshot) + AOF (append-only)
- Eviction Policy: allkeys-lru
- Max Memory: 2GB
- Replicação: Master-Slave (futuro)

### 🐰 RabbitMQ 3 (:5672, :15672)

**Message Broker para Eventos Assíncronos**

**Exchanges:**
- `domain.events` (fanout): Domain Events entre contexts
- `tasks` (direct): Background tasks
- `notifications` (topic): Notificações para usuários

**Queues:**
- `stream.processing`: Processamento de streams
- `ai.detection`: Detecções LPR
- `recording.jobs`: Jobs de gravação
- `notifications.email`: Envio de emails
- `notifications.sms`: Envio de SMS

**Recursos:**
- Dead Letter Queue: Retry de mensagens falhas
- Message TTL: 24 horas
- Persistent messages
- Management UI: :15672

### 📦 MinIO (:9000, :9001)

**Object Storage S3-Compatible**

**Buckets:**
- `recordings`: Vídeos gravados (MP4/HLS)
- `snapshots`: Imagens de câmeras
- `lpr-images`: Placas detectadas
- `exports`: Exports de relatórios
- `thumbnails`: Miniaturas de vídeos

**Recursos:**
- Lifecycle Policies: Retenção de 90 dias
- Versioning: Habilitado para auditoria
- Encryption: Server-side (SSE-S3)
- Access Control: Bucket policies
- Console UI: :9001

### 📊 Prometheus (:9090)

**Coleta e Armazenamento de Métricas**

**Métricas Coletadas:**
- Request rate, latency, errors (RED)
- CPU, memory, disk (USE)
- Stream health (active, bitrate)
- Detection rate (LPR)
- Cache hit rate
- Database connections

**Configuração:**
- Scrape Interval: 15 segundos
- Retention: 15 dias
- Alerting Rules: Configuradas
- Service Discovery: Docker

### 📈 Grafana (:3000)

**Visualização e Alertas**

**Dashboards:**
- System Overview: Visão geral do sistema
- API Performance: Latência e throughput
- Streaming Health: Status dos streams
- AI Detection Stats: Estatísticas de detecção
- Business Metrics: KPIs de negócio

**Alertas:**
- Email notifications
- Slack integration
- PagerDuty (produção)
- Thresholds configuráveis

### 🔍 ELK Stack

**Elasticsearch (:9200)**
- Armazenamento de logs estruturados
- Full-text search
- Retention: 30 dias
- Índices por dia

**Logstash (:5000)**
- Coleta de logs (TCP/UDP)
- Parsing e enrichment
- Filtros por severidade
- Geolocação de IPs

**Kibana (:5601)**
- Visualização de logs
- Dashboards de troubleshooting
- Alertas de erros críticos
- Discover para busca

## Fluxos de Dados Principais

### 1. Autenticação de Usuário
```
Cliente → HAProxy → Kong → Django
Django → PostgreSQL (validar credenciais)
Django → Redis (armazenar sessão)
Django → Cliente (JWT token)
```

### 2. Iniciar Stream de Câmera
```
Cliente → HAProxy → Kong → FastAPI
FastAPI → PostgreSQL (buscar config câmera)
FastAPI → MediaMTX (solicitar proxy)
MediaMTX → Câmera IP (conectar RTSP)
MediaMTX → FastAPI (URL HLS/WebRTC)
FastAPI → RabbitMQ (evento StreamStarted)
FastAPI → Redis (cache status)
FastAPI → Cliente (URL stream)
```

### 3. Detecção de Placas (LPR)
```
Cliente → WebSocket → FastAPI
FastAPI → MediaMTX (subscrever stream)
Loop:
  MediaMTX → FastAPI (frame)
  FastAPI → YOLO (detectar placa)
  FastAPI → MinIO (salvar imagem)
  FastAPI → PostgreSQL (salvar detecção)
  FastAPI → RabbitMQ (evento PlateDetected)
  FastAPI → Cliente (resultado via WS)
```

### 4. Gravação de Vídeo
```
FastAPI → MediaMTX (iniciar gravação)
MediaMTX → MediaMTX (gravar chunks)
MediaMTX → MinIO (upload chunks)
FastAPI → PostgreSQL (metadata)
FastAPI → RabbitMQ (evento RecordingCompleted)
```

## Escalabilidade e Performance

### Horizontal Scaling
- Django: 3+ réplicas atrás do HAProxy
- FastAPI: 3+ réplicas atrás do HAProxy
- PostgreSQL: Read replicas (futuro)
- Redis: Cluster mode (futuro)

### Performance Targets
- API Latency: <100ms (p95)
- Stream Latency: <3s (HLS), <1s (WebRTC)
- LPR Processing: <200ms por frame
- Cache Hit Rate: >80%
- Concurrent Streams: 100+ por instância

### Resource Allocation
- Django: 2 CPU, 4GB RAM por réplica
- FastAPI: 4 CPU, 8GB RAM por réplica
- PostgreSQL: 4 CPU, 16GB RAM
- Redis: 2 CPU, 4GB RAM
- MediaMTX: 4 CPU, 8GB RAM

## Segurança

### Network Security
- SSL/TLS termination no HAProxy
- Internal network isolada
- Firewall rules por serviço

### Application Security
- JWT authentication
- Rate limiting (HAProxy + Kong)
- Input validation (Pydantic + DRF)
- SQL injection prevention (ORM)
- XSS prevention
- CSRF protection

### Data Security
- Encryption at rest (MinIO SSE)
- Encryption in transit (TLS)
- Secrets management (env vars)
- Audit logging
- LGPD compliance

## Monitoramento e Observabilidade

### Métricas (Prometheus + Grafana)
- System metrics (CPU, RAM, Disk)
- Application metrics (requests, latency)
- Business metrics (streams, detections)
- Custom metrics por context

### Logs (ELK Stack)
- Structured logging (JSON)
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Correlation IDs
- Request tracing

### Alertas
- High error rate (>5%)
- High latency (>500ms p95)
- Low cache hit rate (<70%)
- Stream failures
- Disk space (<20%)
- Memory usage (>90%)

## Deployment

### Docker Compose
- Todos os serviços containerizados
- Networks isoladas
- Volumes persistentes
- Health checks
- Restart policies

### CI/CD (Futuro)
- GitHub Actions
- Automated tests
- Docker build e push
- Deploy automático
- Rollback automático

### Infrastructure as Code
- Terraform para AWS
- Ansible para configuração
- Kubernetes para orquestração (futuro)
