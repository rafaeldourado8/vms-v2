# Teste E2E de Streaming e Detecção

Scripts para testar o fluxo completo do GT-Vision VMS sem frontend.

## 🎯 Objetivo

Testar o fluxo completo:
1. **Streaming**: Camera RTSP → Backend → MediaMTX → Player OpenCV
2. **Detecção**: Câmera com IA → Detection API → Armazenamento

---

## 📋 Pré-requisitos

### Instalar OpenCV
```bash
pip install opencv-python
```

### Instalar httpx
```bash
pip install httpx
```

---

## 🚀 Como Executar

### 1. Iniciar Infraestrutura

```bash
# PostgreSQL, Redis, RabbitMQ, MinIO, MediaMTX
scripts\sprint11-setup.bat
```

### 2. Iniciar Backend Django (Terminal 1)

```bash
poetry run python manage.py runserver
```

### 3. Iniciar Streaming API (Terminal 2)

```bash
cd src/streaming
poetry run uvicorn infrastructure.web.main:app --reload --port 8001
```

### 4. Iniciar Detection API (Terminal 3)

```bash
cd src/detection
python main.py
```

Ou:
```bash
poetry run uvicorn src.detection.main:app --reload --port 8002
```

---

## 🎬 Teste 1: Streaming com OpenCV

Simula o fluxo completo de streaming e exibe o vídeo com OpenCV.

```bash
python scripts\test_streaming_e2e.py
```

**O que faz:**
1. ✅ Cria câmera no backend Django
2. ✅ Inicia stream no FastAPI (RTSP → MediaMTX)
3. ✅ Inicia gravação
4. ✅ Abre player OpenCV exibindo o stream
5. ✅ Pressione 'q' para sair

**Stream de teste:** Big Buck Bunny (stream público RTSP)

---

## 🎯 Teste 2: Detecção de Eventos (LPR)

Simula câmera com IA embarcada enviando eventos de detecção.

```bash
python scripts\simulate_camera_detection.py
```

**O que faz:**
1. ✅ Simula câmera com IA embarcada
2. ✅ Detecta placas a cada 3 segundos
3. ✅ Envia eventos via webhook para Detection API
4. ✅ Pressione Ctrl+C para parar

**Placas simuladas:** ABC1234, XYZ5678, DEF9012, etc.

---

## 📊 Verificar Eventos Recebidos

### Via Browser
```
http://localhost:8002/docs
```

### Via cURL

**Listar eventos LPR:**
```bash
curl http://localhost:8002/api/events/lpr
```

**Buscar por placa:**
```bash
curl "http://localhost:8002/api/events/lpr?plate=ABC1234"
```

**Health check:**
```bash
curl http://localhost:8002/health
```

---

## 🏗️ Arquitetura

### Streaming Flow
```
Camera RTSP
    ↓
Django Backend (cria câmera)
    ↓
FastAPI Streaming (inicia stream)
    ↓
MediaMTX (ingestão RTSP → HLS)
    ↓
OpenCV Player (exibe stream)
```

### Detection Flow
```
Camera com IA Embarcada
    ↓
Webhook HTTP POST
    ↓
FastAPI Detection API (porta 8002)
    ↓
Armazenamento (PostgreSQL em produção)
    ↓
Busca e Exibição
```

---

## 🔧 Portas Utilizadas

| Serviço | Porta | URL |
|---------|-------|-----|
| Django Backend | 8000 | http://localhost:8000 |
| Streaming API | 8001 | http://localhost:8001 |
| Detection API | 8002 | http://localhost:8002 |
| MediaMTX HLS | 8889 | http://localhost:8889 |
| MediaMTX RTSP | 8554 | rtsp://localhost:8554 |
| PostgreSQL | 5432 | localhost:5432 |
| Redis | 6379 | localhost:6379 |
| RabbitMQ | 5672 | localhost:5672 |
| MinIO | 9000 | http://localhost:9000 |

---

## 🐛 Troubleshooting

### OpenCV não abre o stream
- Verifique se MediaMTX está rodando: `docker ps`
- Teste o stream RTSP diretamente: `ffplay rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4`

### Detection API não recebe eventos
- Verifique se a API está rodando: `curl http://localhost:8002/health`
- Verifique logs no terminal da Detection API

### Erro ao criar câmera
- Verifique se Django está rodando: `curl http://localhost:8000/health`
- Verifique se PostgreSQL está rodando: `docker ps | findstr postgres`

---

## 📝 Próximos Passos

### Sprint 10b: AI - Webhook LPR (Produção)
- [ ] Integrar Detection API com PostgreSQL
- [ ] Implementar DDD na Detection API
- [ ] Adicionar autenticação JWT
- [ ] Implementar armazenamento de imagens (MinIO)
- [ ] Criar busca avançada de eventos
- [ ] Adicionar exportação de relatórios

### Sprint 9: Mosaico
- [ ] Visualização de múltiplas câmeras
- [ ] Layouts 2x2
- [ ] Salvamento de configurações

---

## ✅ Checklist de Teste

- [ ] Infraestrutura iniciada (PostgreSQL, Redis, RabbitMQ, MinIO, MediaMTX)
- [ ] Django rodando (porta 8000)
- [ ] Streaming API rodando (porta 8001)
- [ ] Detection API rodando (porta 8002)
- [ ] Teste de streaming executado com sucesso
- [ ] Player OpenCV exibiu o vídeo
- [ ] Simulador de detecção enviou eventos
- [ ] Eventos LPR recebidos e listados

---

**Última atualização**: 2025-01-16
