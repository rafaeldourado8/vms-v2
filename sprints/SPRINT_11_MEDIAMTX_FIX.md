# MediaMTX - Correção Aplicada

## ❌ Problema

MediaMTX estava falhando ao iniciar com erro:
```
ERR unable to set read buffer size to 2097152
```

## ✅ Solução

Reduzido o buffer UDP de **2MB (2097152)** para **512KB (524288)** no `mediamtx.yml`.

**Motivo**: Windows/Docker tem limites menores para buffers UDP do que Linux nativo.

## 🔧 Arquivos Corrigidos

- ✅ `mediamtx.yml` - Buffers UDP reduzidos para 512KB

## 🚀 Como Aplicar

### 1. Reiniciar MediaMTX

```bash
# Parar containers
docker-compose -f docker-compose.dev.yml down

# Iniciar novamente
docker-compose -f docker-compose.dev.yml up -d

# Ver logs do MediaMTX
docker-compose -f docker-compose.dev.yml logs -f mediamtx
```

### 2. Validar

Você deve ver no log:
```
INF MediaMTX v1.15.6
INF configuration loaded from /mediamtx.yml
INF [API] listener opened on :9997
INF [metrics] listener opened on :9998
INF [playback] listener opened on :9996
INF [RTSP] listener opened on :8554
INF [HLS] listener opened on :8888
INF [WebRTC] listener opened on :8889
```

**SEM** o erro `ERR unable to set read buffer size`.

## 📊 Buffers Ajustados

| Buffer | Antes | Depois | Motivo |
|--------|-------|--------|--------|
| rtspUDPReadBufferSize | 2MB | 512KB | Limite Windows/Docker |
| mpegtsUDPReadBufferSize | 2MB | 512KB | Limite Windows/Docker |
| rtpUDPReadBufferSize | 2MB | 512KB | Limite Windows/Docker |

**Nota**: 512KB é suficiente para 12 câmeras simultâneas em qualidade HD.

## 🎯 Próximos Passos

Após MediaMTX iniciar corretamente:

```bash
# Verificar todos os serviços
docker-compose -f docker-compose.dev.yml ps

# Deve mostrar 5 containers "Up (healthy)"
```

Depois:

```bash
# Instalar dependências
poetry install

# Aplicar migrations
poetry run python manage.py migrate

# Inicializar MinIO
poetry run python scripts\init_minio.py
```

---

**Execute agora**:
```bash
docker-compose -f docker-compose.dev.yml restart mediamtx
docker-compose -f docker-compose.dev.yml logs -f mediamtx
```
