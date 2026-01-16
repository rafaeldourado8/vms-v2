# Teste E2E com Docker Compose

Teste completo usando containers Docker (sem precisar rodar localmente).

## 🚀 Quick Start

```bash
# Build e teste completo
scripts\docker-test-e2e.bat
```

Isso vai:
1. ✅ Build das imagens (streaming + detection)
2. ✅ Iniciar todos os serviços
3. ✅ Executar testes automatizados
4. ✅ Exibir URLs de acesso

## 📊 Serviços Disponíveis

| Serviço | URL | Descrição |
|---------|-----|-----------|
| Streaming API | http://localhost:8001/docs | API de streaming |
| Detection API | http://localhost:8002/docs | API de detecção |
| MediaMTX HLS | http://localhost:8889 | Servidor HLS |
| Grafana | http://localhost:3000 | Dashboards (admin/admin) |
| Kibana | http://localhost:5601 | Logs |
| RabbitMQ | http://localhost:15672 | Message broker (gtvision/gtvision_password) |
| MinIO | http://localhost:9001 | Storage (minioadmin/minioadmin) |

## 🎬 Testar Streaming Manualmente

### 1. Iniciar stream via API
```bash
curl -X POST http://localhost:8001/api/streams/start \
  -H "Content-Type: application/json" \
  -d "{\"camera_id\":\"123e4567-e89b-12d3-a456-426614174000\",\"source_url\":\"rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4\"}"
```

### 2. Abrir stream no VLC
```
http://localhost:8889/camera_123e4567-e89b-12d3-a456-426614174000/index.m3u8
```

## 🎯 Testar Detecção Manualmente

### 1. Enviar evento LPR
```bash
curl -X POST http://localhost:8002/api/webhooks/lpr \
  -H "Content-Type: application/json" \
  -d "{\"camera_id\":\"123e4567-e89b-12d3-a456-426614174000\",\"plate\":\"ABC1234\",\"confidence\":0.95,\"timestamp\":\"2025-01-16T12:00:00Z\"}"
```

### 2. Listar eventos
```bash
curl http://localhost:8002/api/events/lpr
```

## 🔧 Comandos Úteis

```bash
# Ver logs
docker-compose -f docker-compose.dev.yml logs -f

# Ver logs de um serviço específico
docker-compose -f docker-compose.dev.yml logs -f streaming
docker-compose -f docker-compose.dev.yml logs -f detection

# Parar tudo
docker-compose -f docker-compose.dev.yml down

# Rebuild
docker-compose -f docker-compose.dev.yml build --no-cache

# Restart um serviço
docker-compose -f docker-compose.dev.yml restart streaming
```

## 🐛 Troubleshooting

### Porta já em uso
```bash
# Ver o que está usando a porta
netstat -ano | findstr :8001
```

### Container não inicia
```bash
# Ver logs do container
docker logs gtvision-streaming-dev
docker logs gtvision-detection-dev
```

### Rebuild completo
```bash
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml build --no-cache
docker-compose -f docker-compose.dev.yml up -d
```
