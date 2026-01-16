# Guia de Integração Frontend-Backend

## 🎯 Arquitetura

```
Frontend (React + Vite)
    ↓
HAProxy (porta 80) → Kong Gateway
    ↓
├─→ Django Backend (porta 8000) - Admin + Cidades
├─→ Streaming API (porta 8001) - Streams + Gravações
├─→ Detection API (porta 8002) - Eventos LPR
└─→ MediaMTX (porta 8889) - HLS Streams
```

## 📋 Endpoints Ajustados

### 1. Streaming API (porta 8001)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/streams/start` | Iniciar stream |
| POST | `/api/streams/{id}/stop` | Parar stream |
| GET | `/api/streams/{id}` | Obter stream |
| POST | `/api/recordings/start` | Iniciar gravação |
| POST | `/api/recordings/{id}/stop` | Parar gravação |
| GET | `/api/recordings/{id}` | Obter gravação |
| GET | `/api/recordings/search` | Buscar gravações |
| GET | `/api/timeline` | Obter timeline |
| GET | `/api/recordings/{id}/playback` | URL de playback |
| POST | `/api/recordings/{id}/thumbnails` | Gerar thumbnails |
| POST | `/api/clips` | Criar clipe |
| GET | `/api/clips/{id}` | Obter clipe |
| GET | `/api/clips/{id}/download` | Download clipe |
| POST | `/api/mosaics` | Criar mosaico |
| GET | `/api/mosaics/{id}` | Obter mosaico |
| PUT | `/api/mosaics/{id}` | Atualizar mosaico |
| DELETE | `/api/mosaics/{id}` | Deletar mosaico |
| GET | `/api/users/{id}/mosaics` | Listar mosaicos |

### 2. Detection API (porta 8002)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/webhooks/lpr` | Receber evento LPR |
| POST | `/api/webhooks/object-detection` | Receber detecção |
| GET | `/api/events/lpr` | Listar eventos LPR |
| GET | `/api/events/lpr/{id}` | Obter evento LPR |
| GET | `/api/events/objects` | Listar detecções |

### 3. MediaMTX (porta 8889)

| Tipo | URL | Descrição |
|------|-----|-----------|
| HLS | `http://localhost:8889/camera_{id}/index.m3u8` | Stream HLS |

## 🔧 Configuração Frontend

### 1. Variáveis de Ambiente

Copie `.env.example` para `.env`:

```bash
cd frontend
cp .env.example .env
```

Conteúdo do `.env`:

```env
VITE_API_URL=http://localhost:8000/api
VITE_STREAMING_URL=http://localhost:8001/api
VITE_DETECTION_URL=http://localhost:8002/api
VITE_HLS_URL=http://localhost:8889
VITE_WS_URL=ws://localhost:8001/ws
```

### 2. Instalar Dependências

```bash
cd frontend
npm install
```

### 3. Iniciar Desenvolvimento

```bash
npm run dev
```

Acesse: `http://localhost:5173`

## 📝 Exemplos de Uso

### Iniciar Stream

```typescript
import { streamingService } from '@/services/api'

const cameraId = '123e4567-e89b-12d3-a456-426614174000'
const rtspUrl = 'rtsp://admin:pass@192.168.1.100:554/stream'

const stream = await streamingService.startStream(cameraId, rtspUrl)
console.log('Stream ID:', stream.stream_id)

// URL HLS para player
const hlsUrl = streamingService.getHlsUrl(cameraId)
// http://localhost:8889/camera_123e4567-e89b-12d3-a456-426614174000/index.m3u8
```

### Buscar Timeline

```typescript
const timeline = await streamingService.getTimeline(
  streamId,
  '2025-01-16T00:00:00Z',
  '2025-01-16T23:59:59Z'
)

console.log('Segmentos:', timeline.segments)
console.log('Duração total:', timeline.total_duration_seconds)
console.log('Tem gaps?', timeline.has_gaps)
```

### Listar Eventos LPR

```typescript
import { detectionService } from '@/services/api'

const events = await detectionService.listLprEvents({
  camera_id: cameraId,
  plate: 'ABC1234',
  limit: 100
})

console.log('Eventos:', events.events)
console.log('Total:', events.total)
```

### Criar Mosaico

```typescript
import { mosaicoService } from '@/services/api'

const mosaico = await mosaicoService.create({
  user_id: userId,
  name: 'Mosaico Principal',
  layout: '2x2',
  camera_ids: [camera1Id, camera2Id, camera3Id, camera4Id]
})
```

## 🎥 Player HLS

### Usando Video.js

```typescript
import videojs from 'video.js'

const player = videojs('video-player', {
  controls: true,
  autoplay: false,
  preload: 'auto',
  sources: [{
    src: streamingService.getHlsUrl(cameraId),
    type: 'application/x-mpegURL'
  }]
})
```

### Usando HLS.js

```typescript
import Hls from 'hls.js'

const video = document.getElementById('video')
const hls = new Hls()

hls.loadSource(streamingService.getHlsUrl(cameraId))
hls.attachMedia(video)

hls.on(Hls.Events.MANIFEST_PARSED, () => {
  video.play()
})
```

## 🔐 Autenticação

O frontend já tem interceptor configurado para JWT:

```typescript
// Automático via interceptor
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

## 🚀 Build para Produção

```bash
cd frontend
npm run build
```

Arquivos gerados em `frontend/dist/`

## 📦 Docker

O frontend já tem Dockerfile configurado:

```bash
docker build -t gtvision-frontend ./frontend
docker run -p 80:80 gtvision-frontend
```

## ✅ Checklist de Integração

- [x] Endpoints ajustados no `api.ts`
- [x] Variáveis de ambiente configuradas
- [x] Streaming service atualizado
- [x] Detection service adicionado
- [x] Clip service atualizado
- [x] Mosaico service atualizado
- [x] HLS URL corrigida (porta 8889)
- [ ] Testar com backend rodando
- [ ] Testar autenticação JWT
- [ ] Testar player HLS
- [ ] Testar eventos LPR

## 🐛 Troubleshooting

### CORS Error

Se aparecer erro de CORS, verifique se o backend tem:

```python
# FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### HLS não carrega

1. Verifique se MediaMTX está rodando: `docker ps | findstr mediamtx`
2. Teste URL direta: `http://localhost:8889/camera_ID/index.m3u8`
3. Veja logs: `docker logs gtvision-mediamtx-dev`

### API 404

Verifique se as APIs estão rodando:

```bash
curl http://localhost:8001/health
curl http://localhost:8002/health
```

---

**Última atualização**: 2025-01-16
