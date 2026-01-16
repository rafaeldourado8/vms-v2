# GT-Vision VMS - Arquitetura Completa (Mermaid)

## Diagrama de Arquitetura Geral

```mermaid
graph TB
    subgraph "Cliente Layer"
        CLIENT[🌐 Browser/Mobile<br/>React/Flutter]
    end

    subgraph "Proxy & Gateway Layer"
        HAPROXY[⚖️ HAProxy<br/>:8404<br/>Load Balancer<br/>SSL Termination<br/>Rate Limiting]
        KONG[🦍 Kong Gateway<br/>:8000<br/>API Gateway<br/>Auth/JWT<br/>Rate Limiting<br/>Routing]
    end

    subgraph "Backend Layer - Django"
        DJANGO[🐍 Django 5.0<br/>:8000]
        
        subgraph "Admin Context"
            ADMIN_API[Admin API<br/>DRF]
            ADMIN_DOMAIN[Domain Layer<br/>Users/Roles/Audit]
            ADMIN_INFRA[Infrastructure<br/>PostgreSQL/Redis]
        end
        
        subgraph "Cidades Context"
            CIDADES_API[Cidades API<br/>DRF]
            CIDADES_DOMAIN[Domain Layer<br/>Prefeituras/Cameras]
            CIDADES_INFRA[Infrastructure<br/>PostgreSQL/Redis]
        end
    end

    subgraph "Backend Layer - FastAPI"
        FASTAPI[⚡ FastAPI<br/>:8001]
        
        subgraph "Streaming Context"
            STREAM_API[Streaming API<br/>REST/WebSocket]
            STREAM_DOMAIN[Domain Layer<br/>Streams/Recording]
            STREAM_INFRA[Infrastructure<br/>MediaMTX/MinIO]
        end
        
        subgraph "AI Context"
            AI_API[AI API<br/>REST/WebSocket]
            AI_DOMAIN[Domain Layer<br/>LPR/Analytics]
            AI_INFRA[Infrastructure<br/>YOLO/TensorFlow]
        end
    end

    subgraph "Streaming Layer"
        MEDIAMTX[📹 MediaMTX<br/>RTSP :8554<br/>RTMP :1935<br/>HLS :8888<br/>WebRTC :8889]
        CAMERAS[📷 IP Cameras<br/>RTSP/ONVIF]
    end

    subgraph "Data Layer"
        POSTGRES[(🐘 PostgreSQL 15<br/>:5432<br/>Transactional Data<br/>Metadata)]
        REDIS[(🔴 Redis 7<br/>:6379<br/>Cache<br/>Sessions<br/>Rate Limit)]
        RABBITMQ[🐰 RabbitMQ 3<br/>:5672/:15672<br/>Message Broker<br/>Domain Events<br/>Async Tasks]
        MINIO[📦 MinIO<br/>:9000/:9001<br/>S3 Storage<br/>Videos/Images<br/>Exports]
    end

    subgraph "Observability Layer"
        PROMETHEUS[📊 Prometheus<br/>:9090<br/>Metrics Collection]
        GRAFANA[📈 Grafana<br/>:3000<br/>Dashboards<br/>Alerts]
        ELASTICSEARCH[🔍 Elasticsearch<br/>:9200<br/>Log Storage]
        LOGSTASH[📝 Logstash<br/>:5000<br/>Log Processing]
        KIBANA[📊 Kibana<br/>:5601<br/>Log Visualization]
    end

    %% Client Connections
    CLIENT -->|HTTPS| HAPROXY
    HAPROXY -->|HTTP| KONG
    
    %% Kong Routing
    KONG -->|/api/admin/*<br/>/api/cidades/*| DJANGO
    KONG -->|/api/streaming/*<br/>/api/ai/*<br/>WebSocket| FASTAPI
    
    %% Django Internal
    DJANGO --> ADMIN_API
    DJANGO --> CIDADES_API
    ADMIN_API --> ADMIN_DOMAIN
    ADMIN_DOMAIN --> ADMIN_INFRA
    CIDADES_API --> CIDADES_DOMAIN
    CIDADES_DOMAIN --> CIDADES_INFRA
    
    %% FastAPI Internal
    FASTAPI --> STREAM_API
    FASTAPI --> AI_API
    STREAM_API --> STREAM_DOMAIN
    STREAM_DOMAIN --> STREAM_INFRA
    AI_API --> AI_DOMAIN
    AI_DOMAIN --> AI_INFRA
    
    %% Data Connections - Django
    ADMIN_INFRA -->|SQL| POSTGRES
    ADMIN_INFRA -->|Cache| REDIS
    ADMIN_INFRA -->|Events| RABBITMQ
    CIDADES_INFRA -->|SQL| POSTGRES
    CIDADES_INFRA -->|Cache| REDIS
    CIDADES_INFRA -->|Events| RABBITMQ
    
    %% Data Connections - FastAPI
    STREAM_INFRA -->|SQL| POSTGRES
    STREAM_INFRA -->|Cache| REDIS
    STREAM_INFRA -->|Events| RABBITMQ
    STREAM_INFRA -->|S3 API| MINIO
    STREAM_INFRA -->|RTSP/HLS| MEDIAMTX
    AI_INFRA -->|SQL| POSTGRES
    AI_INFRA -->|Cache| REDIS
    AI_INFRA -->|Events| RABBITMQ
    AI_INFRA -->|S3 API| MINIO
    
    %% Streaming
    CAMERAS -->|RTSP| MEDIAMTX
    MEDIAMTX -->|HLS/WebRTC| CLIENT
    
    %% Observability
    DJANGO -.->|Metrics| PROMETHEUS
    FASTAPI -.->|Metrics| PROMETHEUS
    HAPROXY -.->|Metrics| PROMETHEUS
    KONG -.->|Metrics| PROMETHEUS
    MEDIAMTX -.->|Metrics| PROMETHEUS
    
    PROMETHEUS -->|Query| GRAFANA
    
    DJANGO -.->|Logs| LOGSTASH
    FASTAPI -.->|Logs| LOGSTASH
    LOGSTASH -->|Index| ELASTICSEARCH
    ELASTICSEARCH -->|Query| KIBANA
    
    %% Styling
    classDef clientStyle fill:#bbdefb,stroke:#1e88e5,stroke-width:3px
    classDef proxyStyle fill:#ffe0b2,stroke:#f57c00,stroke-width:3px
    classDef backendStyle fill:#c8e6c9,stroke:#388e3c,stroke-width:3px
    classDef streamStyle fill:#ffcdd2,stroke:#d32f2f,stroke-width:3px
    classDef dataStyle fill:#b3e5fc,stroke:#0277bd,stroke-width:3px
    classDef obsStyle fill:#fff9c4,stroke:#f9a825,stroke-width:3px
    
    class CLIENT clientStyle
    class HAPROXY,KONG proxyStyle
    class DJANGO,FASTAPI,ADMIN_API,CIDADES_API,STREAM_API,AI_API backendStyle
    class MEDIAMTX,CAMERAS streamStyle
    class POSTGRES,REDIS,RABBITMQ,MINIO dataStyle
    class PROMETHEUS,GRAFANA,ELASTICSEARCH,LOGSTASH,KIBANA obsStyle
```

## Diagrama de Fluxo de Dados

```mermaid
sequenceDiagram
    participant C as Cliente
    participant H as HAProxy
    participant K as Kong
    participant D as Django
    participant F as FastAPI
    participant M as MediaMTX
    participant P as PostgreSQL
    participant R as Redis
    participant MQ as RabbitMQ
    participant S3 as MinIO

    Note over C,S3: Fluxo 1: Autenticação
    C->>H: POST /api/admin/auth/login
    H->>K: Forward request
    K->>D: Route to Django
    D->>P: Validate credentials
    P-->>D: User data
    D->>R: Store session
    D-->>K: JWT token
    K-->>H: Response
    H-->>C: JWT token

    Note over C,S3: Fluxo 2: Listar Câmeras
    C->>H: GET /api/cidades/cameras (JWT)
    H->>K: Forward + Auth
    K->>D: Route to Django
    D->>R: Check cache
    alt Cache hit
        R-->>D: Cached data
    else Cache miss
        D->>P: Query cameras
        P-->>D: Camera list
        D->>R: Update cache
    end
    D-->>C: Camera list

    Note over C,S3: Fluxo 3: Iniciar Stream
    C->>H: POST /api/streaming/streams/start
    H->>K: Forward
    K->>F: Route to FastAPI
    F->>P: Get camera config
    P-->>F: RTSP URL
    F->>M: Start stream proxy
    M-->>F: HLS URL
    F->>MQ: Publish StreamStarted event
    F->>R: Cache stream status
    F-->>C: Stream URL (HLS/WebRTC)

    Note over C,S3: Fluxo 4: Processar LPR
    C->>H: WebSocket /api/ai/lpr/stream
    H->>K: Upgrade connection
    K->>F: Route to FastAPI
    F->>M: Subscribe to stream
    loop Frame processing
        M->>F: Video frame
        F->>F: YOLO detection
        F->>P: Save detection
        F->>S3: Save plate image
        F->>MQ: Publish PlateDetected event
        F-->>C: Detection result (WS)
    end

    Note over C,S3: Fluxo 5: Gravação
    F->>M: Request recording
    M->>M: Record stream
    M->>S3: Upload video chunks
    F->>P: Save recording metadata
    F->>MQ: Publish RecordingCompleted event
```

## Diagrama de Bounded Contexts (DDD)

```mermaid
graph LR
    subgraph "Admin Context"
        A_USERS[Users]
        A_ROLES[Roles]
        A_AUDIT[Audit Logs]
        A_USERS --- A_ROLES
        A_USERS --- A_AUDIT
    end

    subgraph "Cidades Context"
        C_PREFEITURAS[Prefeituras]
        C_CAMERAS[Cameras]
        C_LOCATIONS[Locations]
        C_PREFEITURAS --- C_CAMERAS
        C_CAMERAS --- C_LOCATIONS
    end

    subgraph "Streaming Context"
        S_STREAMS[Streams]
        S_RECORDINGS[Recordings]
        S_SNAPSHOTS[Snapshots]
        S_STREAMS --- S_RECORDINGS
        S_STREAMS --- S_SNAPSHOTS
    end

    subgraph "AI Context"
        AI_LPR[LPR Detection]
        AI_ANALYTICS[Analytics]
        AI_ALERTS[Alerts]
        AI_LPR --- AI_ANALYTICS
        AI_LPR --- AI_ALERTS
    end

    subgraph "Shared Kernel"
        SK_EVENTS[Domain Events]
        SK_VALUE[Value Objects]
        SK_EXCEPTIONS[Exceptions]
    end

    %% Context Relationships
    A_USERS -.->|ACL| C_CAMERAS
    C_CAMERAS -.->|ACL| S_STREAMS
    S_STREAMS -.->|ACL| AI_LPR
    
    %% Shared Kernel Usage
    A_AUDIT --> SK_EVENTS
    S_RECORDINGS --> SK_EVENTS
    AI_LPR --> SK_EVENTS
    
    classDef adminStyle fill:#e1bee7,stroke:#7b1fa2
    classDef cidadesStyle fill:#c8e6c9,stroke:#388e3c
    classDef streamStyle fill:#b2dfdb,stroke:#00897b
    classDef aiStyle fill:#ffcdd2,stroke:#d32f2f
    classDef sharedStyle fill:#fff9c4,stroke:#f9a825
    
    class A_USERS,A_ROLES,A_AUDIT adminStyle
    class C_PREFEITURAS,C_CAMERAS,C_LOCATIONS cidadesStyle
    class S_STREAMS,S_RECORDINGS,S_SNAPSHOTS streamStyle
    class AI_LPR,AI_ANALYTICS,AI_ALERTS aiStyle
    class SK_EVENTS,SK_VALUE,SK_EXCEPTIONS sharedStyle
```

## Diagrama de Deployment (Docker)

```mermaid
graph TB
    subgraph "Docker Host"
        subgraph "Network: frontend"
            HAPROXY_C[haproxy:latest<br/>Ports: 80,443,8404]
        end
        
        subgraph "Network: backend"
            KONG_C[kong:3.4<br/>Port: 8000,8001,8443,8444]
            DJANGO_C[django:5.0<br/>Port: 8000<br/>Replicas: 3]
            FASTAPI_C[fastapi:latest<br/>Port: 8001<br/>Replicas: 3]
        end
        
        subgraph "Network: streaming"
            MEDIAMTX_C[mediamtx:latest<br/>Ports: 8554,1935,8888,8889]
        end
        
        subgraph "Network: data"
            POSTGRES_C[postgres:15<br/>Port: 5432<br/>Volume: pgdata]
            REDIS_C[redis:7<br/>Port: 6379<br/>Volume: redisdata]
            RABBITMQ_C[rabbitmq:3-management<br/>Ports: 5672,15672<br/>Volume: rabbitmqdata]
            MINIO_C[minio:latest<br/>Ports: 9000,9001<br/>Volume: miniodata]
        end
        
        subgraph "Network: monitoring"
            PROMETHEUS_C[prometheus:latest<br/>Port: 9090<br/>Volume: prometheus-data]
            GRAFANA_C[grafana:latest<br/>Port: 3000<br/>Volume: grafana-data]
            ELASTICSEARCH_C[elasticsearch:8.11<br/>Port: 9200<br/>Volume: es-data]
            LOGSTASH_C[logstash:8.11<br/>Port: 5000]
            KIBANA_C[kibana:8.11<br/>Port: 5601]
        end
    end
    
    HAPROXY_C --> KONG_C
    KONG_C --> DJANGO_C
    KONG_C --> FASTAPI_C
    DJANGO_C --> POSTGRES_C
    DJANGO_C --> REDIS_C
    DJANGO_C --> RABBITMQ_C
    FASTAPI_C --> POSTGRES_C
    FASTAPI_C --> REDIS_C
    FASTAPI_C --> RABBITMQ_C
    FASTAPI_C --> MINIO_C
    FASTAPI_C --> MEDIAMTX_C
    
    DJANGO_C -.-> PROMETHEUS_C
    FASTAPI_C -.-> PROMETHEUS_C
    PROMETHEUS_C --> GRAFANA_C
    
    DJANGO_C -.-> LOGSTASH_C
    FASTAPI_C -.-> LOGSTASH_C
    LOGSTASH_C --> ELASTICSEARCH_C
    ELASTICSEARCH_C --> KIBANA_C
```

## Descrição Detalhada dos Componentes

### 1. Cliente Layer
- **Tecnologia**: React (Web) / Flutter (Mobile)
- **Responsabilidade**: Interface do usuário, consumo de APIs
- **Comunicação**: HTTPS, WebSocket
- **Autenticação**: JWT Bearer Token

### 2. Proxy & Gateway Layer

#### HAProxy (:8404)
- **Função**: Load Balancer de entrada
- **Recursos**:
  - SSL/TLS Termination
  - Rate Limiting (1000 req/min)
  - Health Checks
  - Sticky Sessions
  - Stats Dashboard (:8404/stats)
- **Algoritmo**: Round Robin com health checks

#### Kong Gateway (:8000)
- **Função**: API Gateway e roteamento
- **Plugins**:
  - JWT Authentication
  - Rate Limiting (100 req/min por IP)
  - CORS
  - Request/Response Transformation
  - Logging
- **Rotas**:
  - `/api/admin/*` → Django
  - `/api/cidades/*` → Django
  - `/api/streaming/*` → FastAPI
  - `/api/ai/*` → FastAPI

### 3. Backend Layer

#### Django 5.0 (:8000)
- **Contexts**: Admin, Cidades
- **Framework**: Django + Django REST Framework
- **Padrão**: DDD (Domain-Driven Design)
- **Camadas**:
  - **API**: Controllers REST (DRF ViewSets)
  - **Application**: Use Cases, DTOs
  - **Domain**: Entities, Value Objects, Domain Services
  - **Infrastructure**: Repositories, ORM, External Services
- **Autenticação**: JWT (djangorestframework-simplejwt)
- **Validação**: Django Forms + Serializers
- **Admin**: Django Admin customizado

**Admin Context**:
- Gestão de usuários e permissões
- Auditoria de ações
- Configurações do sistema
- Multi-tenancy (prefeituras)

**Cidades Context**:
- Cadastro de prefeituras
- Gestão de câmeras
- Localizações e zonas
- Configurações de câmeras

#### FastAPI (:8001)
- **Contexts**: Streaming, AI
- **Framework**: FastAPI + Uvicorn
- **Padrão**: DDD + Async/Await
- **Camadas**:
  - **API**: Routers REST + WebSocket
  - **Application**: Use Cases assíncronos
  - **Domain**: Entities, Aggregates, Domain Events
  - **Infrastructure**: Async Repositories, External APIs
- **WebSocket**: Real-time para streaming e detecções
- **Background Tasks**: Celery + RabbitMQ
- **Validação**: Pydantic Models

**Streaming Context**:
- Proxy de streams RTSP → HLS/WebRTC
- Gravação de vídeos
- Snapshots e thumbnails
- Gestão de sessões de streaming

**AI Context**:
- Detecção de placas (LPR) com YOLO
- Analytics de tráfego
- Alertas inteligentes
- Processamento de frames em tempo real

### 4. Streaming Layer

#### MediaMTX
- **Função**: Servidor de streaming multi-protocolo
- **Protocolos**:
  - **RTSP (:8554)**: Ingestão de câmeras IP
  - **RTMP (:1935)**: Alternativa para ingestão
  - **HLS (:8888)**: Playback em browsers
  - **WebRTC (:8889)**: Baixa latência (<1s)
- **Recursos**:
  - Transcodificação automática
  - Recording em MP4/HLS
  - Authentication via HTTP hooks
  - Metrics para Prometheus

### 5. Data Layer

#### PostgreSQL 15 (:5432)
- **Função**: Database relacional principal
- **Schemas**:
  - `admin`: Users, Roles, Audit
  - `cidades`: Prefeituras, Cameras, Locations
  - `streaming`: Streams, Recordings
  - `ai`: Detections, Analytics, Alerts
- **Recursos**:
  - JSONB para metadados
  - Full-text search
  - Particionamento por data
  - Replicação (futuro)
- **Backup**: Daily automated backups

#### Redis 7 (:6379)
- **Função**: Cache distribuído e session store
- **Uso**:
  - Cache de queries (TTL: 5min)
  - Session storage (JWT blacklist)
  - Rate limiting counters
  - Real-time stream status
  - Pub/Sub para notificações
- **Persistência**: RDB + AOF

#### RabbitMQ 3 (:5672, :15672)
- **Função**: Message broker para eventos assíncronos
- **Exchanges**:
  - `domain.events`: Domain Events (fanout)
  - `tasks`: Background tasks (direct)
  - `notifications`: User notifications (topic)
- **Queues**:
  - `stream.processing`: Processamento de streams
  - `ai.detection`: Detecções LPR
  - `recording.jobs`: Jobs de gravação
  - `notifications.email`: Envio de emails
- **Dead Letter Queue**: Para retry de mensagens

#### MinIO (:9000, :9001)
- **Função**: Object storage S3-compatible
- **Buckets**:
  - `recordings`: Vídeos gravados (MP4/HLS)
  - `snapshots`: Imagens de câmeras
  - `lpr-images`: Placas detectadas
  - `exports`: Exports de relatórios
- **Lifecycle**: Retenção de 90 dias
- **Versioning**: Habilitado
- **Encryption**: Server-side (SSE)

### 6. Observability Layer

#### Prometheus (:9090)
- **Função**: Coleta e armazenamento de métricas
- **Métricas**:
  - Request rate, latency, errors (RED)
  - CPU, memory, disk (USE)
  - Custom business metrics
- **Scrape Interval**: 15s
- **Retention**: 15 dias

#### Grafana (:3000)
- **Função**: Visualização e alertas
- **Dashboards**:
  - System Overview
  - API Performance
  - Streaming Health
  - AI Detection Stats
  - Business Metrics
- **Alertas**: Email, Slack, PagerDuty

#### ELK Stack

**Elasticsearch (:9200)**:
- Armazenamento de logs
- Full-text search
- Retention: 30 dias

**Logstash (:5000)**:
- Coleta e processamento de logs
- Parsing e enrichment
- Filtros por severidade

**Kibana (:5601)**:
- Visualização de logs
- Dashboards de troubleshooting
- Alertas de erros

## Fluxos Principais

### Fluxo 1: Autenticação
1. Cliente envia credenciais para `/api/admin/auth/login`
2. HAProxy encaminha para Kong
3. Kong roteia para Django
4. Django valida no PostgreSQL
5. Django gera JWT e armazena session no Redis
6. Cliente recebe JWT para requests subsequentes

### Fluxo 2: Iniciar Stream
1. Cliente solicita stream via `/api/streaming/streams/start`
2. Kong autentica JWT e roteia para FastAPI
3. FastAPI busca config da câmera no PostgreSQL
4. FastAPI solicita proxy do stream no MediaMTX
5. MediaMTX conecta na câmera via RTSP
6. MediaMTX gera URL HLS/WebRTC
7. FastAPI publica evento `StreamStarted` no RabbitMQ
8. FastAPI retorna URL para cliente

### Fluxo 3: Detecção LPR
1. Cliente conecta WebSocket em `/api/ai/lpr/stream`
2. FastAPI subscreve ao stream no MediaMTX
3. Para cada frame:
   - FastAPI processa com YOLO
   - Detecta placas
   - Salva imagem no MinIO
   - Salva detecção no PostgreSQL
   - Publica evento `PlateDetected` no RabbitMQ
   - Envia resultado via WebSocket para cliente

### Fluxo 4: Gravação
1. FastAPI solicita gravação ao MediaMTX
2. MediaMTX grava chunks de vídeo
3. MediaMTX faz upload para MinIO
4. FastAPI salva metadata no PostgreSQL
5. Ao finalizar, publica evento `RecordingCompleted`

## Escalabilidade

- **Horizontal**: Django e FastAPI com múltiplas réplicas
- **Load Balancing**: HAProxy distribui carga
- **Cache**: Redis reduz load no PostgreSQL
- **Async**: RabbitMQ para processamento assíncrono
- **Storage**: MinIO escalável com múltiplos nodes

## Segurança

- **SSL/TLS**: Terminação no HAProxy
- **JWT**: Autenticação stateless
- **Rate Limiting**: HAProxy + Kong
- **CORS**: Configurado no Kong
- **Input Validation**: Pydantic + DRF Serializers
- **SQL Injection**: ORM (Django ORM + SQLAlchemy)
- **Secrets**: Variáveis de ambiente + Vault (futuro)

## Performance

- **Cache Hit Rate**: >80% (Redis)
- **API Latency**: <100ms (p95)
- **Stream Latency**: <3s (HLS), <1s (WebRTC)
- **LPR Processing**: <200ms por frame
- **Database Connections**: Pool de 20 conexões
- **Concurrent Streams**: 100+ por instância FastAPI
