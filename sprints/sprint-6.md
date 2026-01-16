# Sprint 6 - Gravação Cíclica

**Duração**: 10 dias  
**Objetivo**: Sistema de gravação contínua com retenção por plano

---

## 🎯 Objetivos

1. Gravação contínua RTSP → MP4/FMP4
2. Retenção: 7/15/30 dias (por plano)
3. Armazenamento S3/MinIO
4. Worker RabbitMQ para processamento assíncrono
5. Limpeza automática de arquivos antigos

---

## 📋 Entregáveis

### Domain Layer
- [ ] Recording entity
- [ ] RecordingStatus enum (RECORDING, STOPPED, ERROR)
- [ ] RetentionPolicy value object (7/15/30 dias)
- [ ] RecordingRepository interface

### Application Layer
- [ ] StartRecordingUseCase
- [ ] StopRecordingUseCase
- [ ] GetRecordingUseCase
- [ ] SearchRecordingsUseCase
- [ ] DTOs (StartRecordingDTO, RecordingResponseDTO)

### Infrastructure Layer
- [ ] FFmpeg wrapper (gravação RTSP → MP4)
- [ ] S3/MinIO client
- [ ] RabbitMQ worker (processamento assíncrono)
- [ ] FastAPI endpoints:
  - POST /api/recordings/start
  - POST /api/recordings/{id}/stop
  - GET /api/recordings/{id}
  - GET /api/recordings/search
- [ ] Cron job para limpeza automática

### Testes
- [ ] 10 testes unitários
- [ ] 5 testes de integração

---

## 🔧 Tecnologias

### FFmpeg
```bash
ffmpeg -i rtsp://camera \
  -c:v copy -c:a copy \
  -f segment -segment_time 3600 \
  -strftime 1 \
  output_%Y%m%d_%H%M%S.mp4
```

### MinIO (S3-compatible)
```yaml
minio:
  image: minio/minio
  command: server /data --console-address ":9001"
  ports:
    - "9000:9000"
    - "9001:9001"
```

### RabbitMQ Worker
```python
# Consumir mensagens de gravação
channel.basic_consume(
    queue='recordings',
    on_message_callback=process_recording
)
```

---

## 📡 API Endpoints

### POST /api/recordings/start
Inicia gravação de um stream

**Request**:
```json
{
  "stream_id": "cam-001",
  "retention_days": 7
}
```

**Response**:
```json
{
  "recording_id": "uuid",
  "stream_id": "cam-001",
  "status": "RECORDING",
  "started_at": "2025-01-15T10:00:00Z",
  "retention_days": 7,
  "storage_path": "s3://bucket/cam-001/2025/01/15/"
}
```

### POST /api/recordings/{id}/stop
Para gravação

**Response**:
```json
{
  "recording_id": "uuid",
  "status": "STOPPED",
  "stopped_at": "2025-01-15T11:00:00Z",
  "duration_seconds": 3600,
  "file_size_mb": 1024
}
```

### GET /api/recordings/search
Busca gravações por período

**Query Params**:
- camera_id
- start_date
- end_date

**Response**:
```json
{
  "recordings": [
    {
      "recording_id": "uuid",
      "stream_id": "cam-001",
      "started_at": "2025-01-15T10:00:00Z",
      "duration_seconds": 3600,
      "file_size_mb": 1024,
      "storage_path": "s3://..."
    }
  ],
  "total": 10
}
```

---

## 🎬 Fluxo de Gravação

1. Cliente chama `POST /api/recordings/start`
2. Backend publica mensagem no RabbitMQ
3. Worker consome mensagem
4. Worker inicia FFmpeg (RTSP → MP4)
5. Arquivos salvos no S3/MinIO
6. Metadata salvo no PostgreSQL
7. Cron job limpa arquivos antigos (retention policy)

---

## 🗄️ Estrutura S3

```
bucket/
├── cam-001/
│   ├── 2025/
│   │   ├── 01/
│   │   │   ├── 15/
│   │   │   │   ├── 10_00_00.mp4
│   │   │   │   ├── 11_00_00.mp4
│   │   │   │   └── 12_00_00.mp4
```

---

## 🧪 Testes

### Unitários (10)
- Recording entity
- RetentionPolicy value object
- StartRecordingUseCase
- StopRecordingUseCase

### Integração (5)
- FFmpeg recording
- S3 upload
- RabbitMQ worker
- Cleanup job
- API endpoints

---

## 📊 Métricas de Sucesso

- ✅ Gravação contínua funcionando
- ✅ Arquivos no S3/MinIO
- ✅ Limpeza automática (retention)
- ✅ Worker RabbitMQ processando
- ✅ Cobertura > 90%

---

## 🚀 Implementação Simplificada (MVP)

Para MVP, vamos simplificar:
1. ✅ Gravação local (sem S3 inicialmente)
2. ✅ FFmpeg direto (sem RabbitMQ inicialmente)
3. ✅ Limpeza manual (sem cron inicialmente)
4. ✅ Endpoints básicos funcionando

---

**Status**: 🚀 PRONTA PARA INICIAR
