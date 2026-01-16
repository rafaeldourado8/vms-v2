# Sprint 11 - Guia de Integração Real

**Data**: 2025-01-15  
**Status**: 📋 PLANEJADA  
**Objetivo**: Migrar de in-memory para PostgreSQL + RabbitMQ + MinIO + Docker

---

## 🎯 Visão Geral

Migrar todos os repositórios in-memory para PostgreSQL, configurar RabbitMQ real, MinIO real e Docker Compose funcional.

---

## 📊 Escopo da Integração

### Repositórios a Migrar (10)

#### Admin Context
1. **UserRepository** → PostgreSQL
2. **RoleRepository** → PostgreSQL

#### Cidades Context
3. **CidadeRepository** → PostgreSQL
4. **CameraRepository** → PostgreSQL

#### Streaming Context
5. **StreamRepository** → PostgreSQL
6. **RecordingRepository** → PostgreSQL
7. **ClipRepository** → PostgreSQL
8. **MosaicRepository** → PostgreSQL

#### AI Context
9. **LPREventRepository** → PostgreSQL

### Serviços a Integrar (3)
1. **MessageBroker** → RabbitMQ real
2. **StorageService** → MinIO real
3. **Cache** → Redis real

---

## 🗄️ PostgreSQL - Migrations

### 1. Admin Context

```sql
-- users table
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- roles table
CREATE TABLE roles (
    id UUID PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    permissions JSONB
);

-- user_roles table
CREATE TABLE user_roles (
    user_id UUID REFERENCES users(id),
    role_id UUID REFERENCES roles(id),
    PRIMARY KEY (user_id, role_id)
);
```

### 2. Cidades Context

```sql
-- cidades table
CREATE TABLE cidades (
    id UUID PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    estado VARCHAR(2) NOT NULL,
    plano_retencao_dias INTEGER CHECK (plano_retencao_dias IN (7, 15, 30)),
    created_at TIMESTAMP DEFAULT NOW()
);

-- cameras table
CREATE TABLE cameras (
    id UUID PRIMARY KEY,
    cidade_id UUID REFERENCES cidades(id) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    url_rtsp VARCHAR(500) NOT NULL,
    localizacao VARCHAR(500),
    status VARCHAR(20) DEFAULT 'INATIVA',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_cameras_cidade ON cameras(cidade_id);
```

### 3. Streaming Context

```sql
-- streams table
CREATE TABLE streams (
    id UUID PRIMARY KEY,
    camera_id UUID NOT NULL,
    source_url VARCHAR(500) NOT NULL,
    status VARCHAR(20) DEFAULT 'STOPPED',
    started_at TIMESTAMP,
    stopped_at TIMESTAMP
);

-- recordings table
CREATE TABLE recordings (
    id UUID PRIMARY KEY,
    stream_id UUID NOT NULL,
    retention_days INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'RECORDING',
    started_at TIMESTAMP DEFAULT NOW(),
    stopped_at TIMESTAMP,
    storage_path VARCHAR(500),
    file_size_mb DECIMAL(10,2) DEFAULT 0,
    duration_seconds INTEGER DEFAULT 0
);

CREATE INDEX idx_recordings_stream ON recordings(stream_id);
CREATE INDEX idx_recordings_stopped_at ON recordings(stopped_at);

-- clips table
CREATE TABLE clips (
    id UUID PRIMARY KEY,
    recording_id UUID NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    storage_path VARCHAR(500),
    file_size_mb DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_clips_recording ON clips(recording_id);

-- mosaics table
CREATE TABLE mosaics (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    layout VARCHAR(20) DEFAULT '2x2',
    camera_ids JSONB
);

CREATE INDEX idx_mosaics_user ON mosaics(user_id);
```

### 4. AI Context

```sql
-- lpr_events table
CREATE TABLE lpr_events (
    id UUID PRIMARY KEY,
    camera_id UUID NOT NULL,
    plate VARCHAR(8) NOT NULL,
    confidence DECIMAL(3,2) NOT NULL,
    image_url VARCHAR(500),
    detected_at TIMESTAMP DEFAULT NOW(),
    city_id UUID
);

CREATE INDEX idx_lpr_plate ON lpr_events(plate);
CREATE INDEX idx_lpr_camera ON lpr_events(camera_id);
CREATE INDEX idx_lpr_city ON lpr_events(city_id);
CREATE INDEX idx_lpr_detected_at ON lpr_events(detected_at);
```

---

## 🔧 Implementação - PostgreSQL Repositories

### Exemplo: StreamRepositoryPostgreSQL

```python
"""Stream repository PostgreSQL implementation."""
from uuid import UUID
from typing import List, Optional
from sqlalchemy import select
from src.streaming.domain.entities.stream import Stream
from src.streaming.domain.repositories.stream_repository import StreamRepository
from src.shared_kernel.infrastructure.database import Database


class StreamRepositoryPostgreSQL(StreamRepository):
    """PostgreSQL stream repository implementation."""
    
    def __init__(self, db: Database):
        self.db = db
    
    async def save(self, entity: Stream) -> Stream:
        """Save stream."""
        async with self.db.session() as session:
            # Insert or update logic
            await session.execute(
                """
                INSERT INTO streams (id, camera_id, source_url, status, started_at, stopped_at)
                VALUES (:id, :camera_id, :source_url, :status, :started_at, :stopped_at)
                ON CONFLICT (id) DO UPDATE SET
                    status = EXCLUDED.status,
                    stopped_at = EXCLUDED.stopped_at
                """,
                {
                    "id": entity.id,
                    "camera_id": entity.camera_id,
                    "source_url": entity.source_url,
                    "status": entity.status.value,
                    "started_at": entity.started_at,
                    "stopped_at": entity.stopped_at
                }
            )
            await session.commit()
        return entity
    
    async def find_by_id(self, id: UUID) -> Optional[Stream]:
        """Find stream by ID."""
        async with self.db.session() as session:
            result = await session.execute(
                "SELECT * FROM streams WHERE id = :id",
                {"id": id}
            )
            row = result.fetchone()
            if not row:
                return None
            
            return Stream(
                id=row.id,
                camera_id=row.camera_id,
                source_url=row.source_url,
                status=StreamStatus(row.status),
                started_at=row.started_at,
                stopped_at=row.stopped_at
            )
```

---

## 🐰 RabbitMQ - Configuração Real

### 1. Atualizar MessageBroker

```python
"""Message broker implementation using RabbitMQ."""
import aio_pika
import json
from typing import Callable
from src.shared_kernel.infrastructure.logger import Logger


class RabbitMQMessageBroker:
    """RabbitMQ message broker implementation."""
    
    def __init__(self, url: str = "amqp://gtvision:gtvision_password@rabbitmq:5672/"):
        self.url = url
        self.logger = Logger(__name__)
        self.connection = None
        self.channel = None
    
    async def connect(self):
        """Connect to RabbitMQ."""
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()
    
    async def publish(self, exchange: str, routing_key: str, message: dict):
        """Publish message."""
        if not self.channel:
            await self.connect()
        
        exchange_obj = await self.channel.declare_exchange(
            exchange,
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
        
        await exchange_obj.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                content_type="application/json"
            ),
            routing_key=routing_key
        )
    
    async def consume(self, queue: str, callback: Callable):
        """Consume messages."""
        if not self.channel:
            await self.connect()
        
        queue_obj = await self.channel.declare_queue(queue, durable=True)
        
        async with queue_obj.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = json.loads(message.body.decode())
                    await callback(data)
```

### 2. Workers

Atualizar workers para usar RabbitMQ real:
- `RecordingWorker`
- `ClipWorker`

---

## 📦 MinIO - Configuração Real

### 1. Verificar MinIOStorageService

Já implementado em `storage_service_impl.py` - apenas validar configuração.

### 2. Buckets

```python
# Criar buckets no startup
buckets = ["recordings", "clips", "lpr-images", "thumbnails"]
for bucket in buckets:
    if not storage_service.client.bucket_exists(bucket):
        storage_service.client.make_bucket(bucket)
```

---

## 🐳 Docker Compose - Atualização

### 1. Adicionar MinIO

```yaml
minio:
  image: minio/minio:latest
  command: server /data --console-address ":9001"
  ports:
    - "9000:9000"
    - "9001:9001"
  environment:
    MINIO_ROOT_USER: minioadmin
    MINIO_ROOT_PASSWORD: minioadmin
  volumes:
    - minio_data:/data
  networks:
    - gtvision
```

### 2. Atualizar Backend Services

```yaml
backend:
  build:
    context: .
    dockerfile: docker/backend/Dockerfile
  environment:
    - DB_HOST=postgres
    - REDIS_HOST=redis
    - RABBITMQ_HOST=rabbitmq
    - STORAGE_ENDPOINT=http://minio:9000
  depends_on:
    - postgres
    - redis
    - rabbitmq
    - minio
```

---

## 🧪 Testes de Integração

### 1. Criar test_integration.py

```python
"""Integration tests."""
import pytest
from uuid import uuid4
from src.streaming.infrastructure.persistence.stream_repository_postgresql import StreamRepositoryPostgreSQL
from src.streaming.domain.entities.stream import Stream


@pytest.mark.integration
async def test_stream_repository_postgresql(db):
    """Test PostgreSQL stream repository."""
    repository = StreamRepositoryPostgreSQL(db)
    
    stream = Stream(
        id=uuid4(),
        camera_id=uuid4(),
        source_url="rtsp://test"
    )
    
    await repository.save(stream)
    found = await repository.find_by_id(stream.id)
    
    assert found is not None
    assert found.id == stream.id
```

---

## 📝 Checklist de Implementação

### PostgreSQL
- [ ] Criar migrations (Alembic)
- [ ] Implementar 9 repositories PostgreSQL
- [ ] Testes de integração para cada repository
- [ ] Connection pooling
- [ ] Error handling

### RabbitMQ
- [ ] Atualizar MessageBroker para RabbitMQ real
- [ ] Configurar exchanges e queues
- [ ] Atualizar RecordingWorker
- [ ] Atualizar ClipWorker
- [ ] Dead letter queues

### MinIO
- [ ] Validar MinIOStorageService
- [ ] Criar buckets no startup
- [ ] Lifecycle policies (retention)
- [ ] Backup strategy

### Docker
- [ ] Atualizar docker-compose.yml
- [ ] Health checks
- [ ] Volumes persistence
- [ ] Networks configuration
- [ ] Environment variables

### Testes
- [ ] 20+ testes de integração
- [ ] Testes E2E básicos
- [ ] Load testing (opcional)

---

## 🚀 Ordem de Implementação

1. **PostgreSQL** (2 dias)
   - Migrations
   - Repositories
   - Testes

2. **RabbitMQ** (1 dia)
   - MessageBroker
   - Workers
   - Testes

3. **MinIO** (0.5 dia)
   - Validação
   - Buckets
   - Policies

4. **Docker** (1 dia)
   - docker-compose.yml
   - Health checks
   - Testes E2E

5. **Validação Final** (0.5 dia)
   - Smoke tests
   - Documentação

**Total**: ~5 dias

---

## 📊 Métricas de Sucesso

- ✅ Todos os repositories usando PostgreSQL
- ✅ RabbitMQ processando mensagens
- ✅ MinIO armazenando arquivos
- ✅ Docker Compose up funcionando
- ✅ 20+ testes de integração passando
- ✅ Cobertura >80% em integração

---

**Status**: 📋 GUIA COMPLETO - Pronto para implementação quando ambiente estiver configurado
