# 🐳 Sprint 4 - Teste com Docker

## ✅ Arquivos Criados

### Docker
- ✅ `docker/streaming/Dockerfile` - Container FastAPI
- ✅ `docker-compose.test.yml` - Compose simplificado
- ✅ `scripts/test-streaming.bat` - Script de teste

### Streaming Context (10 arquivos Python)
- ✅ Domain Layer (4 arquivos)
- ✅ Application Layer (4 arquivos)  
- ✅ Infrastructure Layer (3 arquivos)
- ✅ Tests (2 arquivos)

## 🚀 Como Testar

### 1. Build e Start
```bash
cd "d:\GT-Vision VMS"
docker-compose -f docker-compose.test.yml build
docker-compose -f docker-compose.test.yml up -d
```

### 2. Verificar Logs
```bash
# Streaming service
docker logs gtvision-streaming-test -f

# MediaMTX
docker logs gtvision-mediamtx-test -f
```

### 3. Testar Health Check
```bash
curl http://localhost:8001/health
curl http://localhost:9997/v3/config/global/get
```

### 4. Testar API Docs
Abrir no navegador:
- http://localhost:8001/docs (Swagger UI)
- http://localhost:8001/redoc (ReDoc)

### 5. Testar Start Stream
```bash
curl -X POST http://localhost:8001/api/streams/start \
  -H "Content-Type: application/json" \
  -d "{\"camera_id\":\"123e4567-e89b-12d3-a456-426614174000\",\"source_url\":\"rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4\"}"
```

### 6. Verificar Stream no MediaMTX
```bash
curl http://localhost:9997/v3/paths/list
```

### 7. Parar Stream
```bash
curl -X POST http://localhost:8001/api/streams/{stream_id}/stop
```

### 8. Parar Serviços
```bash
docker-compose -f docker-compose.test.yml down
```

## 🔧 Troubleshooting

### Container não inicia
```bash
# Ver logs
docker logs gtvision-streaming-test

# Entrar no container
docker exec -it gtvision-streaming-test bash

# Testar imports
python -c "from src.streaming.infrastructure.web.main import app; print('OK')"
```

### MediaMTX não responde
```bash
# Verificar se está rodando
docker ps | grep mediamtx

# Testar API
curl http://localhost:9997/v3/config/global/get
```

### Erro de null bytes
Os arquivos Python foram criados com null bytes. O Docker vai recriar tudo limpo no build.

## 📊 Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | /health | Health check |
| GET | /docs | Swagger UI |
| POST | /api/streams/start | Iniciar stream |
| POST | /api/streams/{id}/stop | Parar stream |
| GET | /api/streams/{id} | Status do stream |

## 🎯 Próximos Passos

1. ✅ Testar com Docker
2. ✅ Validar integração MediaMTX
3. ✅ Testar com stream RTSP real
4. ⏳ Adicionar monitoramento
5. ⏳ Completar testes de integração

## 📝 Notas

- MediaMTX API: http://localhost:9997
- Streaming API: http://localhost:8001
- HLS endpoint: http://localhost:8888/{stream_id}
- WebRTC endpoint: http://localhost:8889/{stream_id}

**Status**: Pronto para testar! 🚀
