# Sprint 5 - Streaming Context (HLS/WebRTC Zero Latência)

**Duração**: 10 dias  
**Objetivo**: Streaming de alta qualidade com latência ultra-baixa

---

## 🎯 Objetivos

1. Configurar MediaMTX para HLS otimizado
2. Implementar WebRTC para latência zero
3. API para obter URLs de streaming
4. Fallback automático HLS ↔ WebRTC
5. Métricas de qualidade (bitrate, fps, latência)

---

## 📋 Entregáveis

### Domain Layer
- [ ] StreamQuality value object (bitrate, fps, latência)
- [ ] StreamProtocol enum (HLS, WEBRTC)
- [ ] StreamURL value object

### Application Layer
- [ ] GetStreamURLUseCase (retorna HLS + WebRTC URLs)
- [ ] GetStreamMetricsUseCase (qualidade do stream)
- [ ] DTOs (StreamURLDTO, StreamMetricsDTO)

### Infrastructure Layer
- [ ] MediaMTX HLS configuration (otimizado)
- [ ] MediaMTX WebRTC configuration
- [ ] FastAPI endpoints:
  - GET /api/streams/{id}/urls (HLS + WebRTC)
  - GET /api/streams/{id}/metrics
  - WS /api/streams/{id}/events
- [ ] WebSocket para eventos em tempo real

### Testes
- [ ] 10 testes unitários
- [ ] 5 testes de integração
- [ ] Testes de latência (benchmark)

### Documentação
- [ ] Guia de configuração MediaMTX
- [ ] Exemplos de integração (player)
- [ ] Troubleshooting

---

## 🔧 Configuração MediaMTX

### HLS Otimizado
```yaml
hls: yes
hlsAddress: :8888
hlsSegmentCount: 10
hlsSegmentDuration: 2s
hlsPartDuration: 500ms
hlsVariant: fmp4
```

### WebRTC
```yaml
webrtc: yes
webrtcAddress: :8889
webrtcLocalUDPAddress: :8189
webrtcIPsFromInterfaces: yes
```

---

## 📡 API Endpoints

### GET /api/streams/{stream_id}/urls
Retorna URLs HLS e WebRTC

**Response**:
```json
{
  "stream_id": "uuid",
  "hls_url": "http://localhost:8888/{stream_id}",
  "webrtc_url": "http://localhost:8889/{stream_id}",
  "rtsp_url": "rtsp://localhost:8554/{stream_id}",
  "status": "RUNNING"
}
```

### GET /api/streams/{stream_id}/metrics
Retorna métricas de qualidade

**Response**:
```json
{
  "stream_id": "uuid",
  "bitrate": 2500000,
  "fps": 30,
  "latency_ms": 150,
  "resolution": "1920x1080",
  "codec": "H264"
}
```

### WS /api/streams/{stream_id}/events
WebSocket para eventos em tempo real

**Events**:
```json
{
  "type": "quality_change",
  "bitrate": 2000000,
  "fps": 25
}
```

---

## 🎬 Fluxo de Uso

1. Cliente chama `POST /api/streams/start`
2. Backend inicia stream no MediaMTX
3. Cliente chama `GET /api/streams/{id}/urls`
4. Cliente recebe URLs HLS + WebRTC
5. Player tenta WebRTC primeiro (baixa latência)
6. Se falhar, fallback para HLS
7. WebSocket envia eventos de qualidade

---

## 🧪 Testes

### Unitários (10)
- StreamQuality value object
- StreamProtocol enum
- GetStreamURLUseCase
- GetStreamMetricsUseCase

### Integração (5)
- GET /urls endpoint
- GET /metrics endpoint
- WebSocket connection
- HLS playback
- WebRTC playback

### Performance
- Latência HLS: < 3s
- Latência WebRTC: < 500ms
- Throughput: > 100 streams simultâneos

---

## 📊 Métricas de Sucesso

- ✅ HLS funcionando com < 3s latência
- ✅ WebRTC funcionando com < 500ms latência
- ✅ Fallback automático
- ✅ 100 streams simultâneos
- ✅ Cobertura > 90%

---

## 🚀 Próximos Passos (Sprint 6)

- Gravação cíclica
- Retenção por plano (7/15/30 dias)
- Armazenamento S3/MinIO
- Limpeza automática

---

**Status**: 🚀 PRONTA PARA INICIAR
