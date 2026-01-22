# Streaming Context

Bounded Context responsável pela ingestão e distribuição de streams de vídeo.

## 🎯 Responsabilidades

- Ingestão de streams RTSP/RTMP
- Integração com MediaMTX
- Controle de streams (start/stop)
- Monitoramento de status
- Transcodificação HLS/WebRTC (futuro)

## 🏗️ Arquitetura

```
streaming/
├── domain/              # Lógica de negócio
│   ├── entities/       # Stream
│   ├── value_objects/  # StreamStatus
│   ├── repositories/   # StreamRepository
│   └── services/       # MediaMTXClient
├── application/        # Casos de uso
│   ├── use_cases/     # StartStream, StopStream
│   └── dtos/          # DTOs
└── infrastructure/     # Implementações
    ├── external_services/  # MediaMTX HTTP client
    ├── persistence/        # Repository impl
    └── web/               # FastAPI app
```

## 🚀 Quick Start

### 1. Iniciar MediaMTX

```bash
docker-compose up -d mediamtx
```

### 2. Iniciar Streaming API

```bash
cd src/streaming/infrastructure/web
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### 3. Testar API

```bash
# Health check
curl http://localhost:8001/health

# Iniciar stream
curl -X POST http://localhost:8001/api/streams/start \
  -H "Content-Type: application/json" \
  -d '{
    "camera_id": "123e4567-e89b-12d3-a456-426614174000",
    "source_url": "rtsp://admin:pass@192.168.1.100:554/stream"
  }'

# Obter status
curl http://localhost:8001/api/streams/{stream_id}

# Parar stream
curl -X POST http://localhost:8001/api/streams/{stream_id}/stop
```

## 📡 Endpoints

### POST /api/streams/start
Iniciar ingestão de stream

**Request**:
```json
{
  "camera_id": "uuid",
  "source_url": "rtsp://admin:pass@192.168.1.100:554/stream"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "camera_id": "uuid",
  "source_url": "rtsp://...",
  "status": "RUNNING",
  "started_at": "2025-01-15T10:00:00Z",
  "stopped_at": null
}
```

### POST /api/streams/{stream_id}/stop
Parar stream

**Response** (204): No content

### GET /api/streams/{stream_id}
Obter status do stream

**Response** (200):
```json
{
  "id": "uuid",
  "camera_id": "uuid",
  "source_url": "rtsp://...",
  "status": "RUNNING",
  "started_at": "2025-01-15T10:00:00Z",
  "stopped_at": null
}
```

## 🔧 Configuração

### MediaMTX

```yaml
# mediamtx.yml
api: yes
apiAddress: :9997

paths:
  all:
    source: publisher
    sourceOnDemand: no
```

### Environment Variables

```env
MEDIAMTX_URL=http://mediamtx:9997
MEDIAMTX_TIMEOUT=10
```

## 🧪 Testes

```bash
# Testes unitários
pytest src/streaming/tests/unit -v

# Testes de integração
pytest src/streaming/tests/integration -v

# Com cobertura
pytest src/streaming --cov=src/streaming --cov-report=html
```

## 📊 Status de Streams

| Status | Descrição |
|--------|-----------|
| STOPPED | Stream parado |
| STARTING | Iniciando conexão |
| RUNNING | Stream ativo |
| ERROR | Erro na conexão |

## 🔒 Regras de Negócio

1. **Stream Único**: Apenas 1 stream ativo por câmera
2. **Validação**: Source URL deve ser RTSP ou RTMP
3. **Timeout**: Conexão com MediaMTX tem timeout de 10s
4. **Retry**: Não há retry automático (implementar em Sprint futura)

## 🎯 Roadmap

### Sprint 4 (Atual) ✅
- [x] Ingestão RTSP/RTMP
- [x] Controle de streams
- [x] FastAPI endpoints
- [ ] Monitoramento

### Sprint 5 (Próxima)
- [ ] Transcodificação HLS
- [ ] WebRTC signaling
- [ ] Player web
- [ ] Latência baixa

### Sprint 6 (Futuro)
- [ ] Gravação de vídeo
- [ ] Snapshots
- [ ] Replay
- [ ] Retenção cíclica

## 📚 Referências

- [MediaMTX](https://github.com/bluenviron/mediamtx)
- [FastAPI](https://fastapi.tiangolo.com/)
- [RTSP Protocol](https://datatracker.ietf.org/doc/html/rfc2326)
- [HLS Specification](https://datatracker.ietf.org/doc/html/rfc8216)
