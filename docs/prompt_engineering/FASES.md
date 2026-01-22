# Fases de Refatoração - GT-Vision VMS v2

## ✅ FASE 1: Fundação & Limpeza (CONCLUÍDA)

### Objetivos
- Remover infraestrutura obsoleta (Kong, HAProxy, ELK)
- Simplificar arquitetura para Nginx como gateway único
- Reorganizar estrutura de pastas seguindo DDD
- Atualizar documentação

### Executado

#### 1.1 Limpeza de Legado
- ✅ Removido: `kong/`, `haproxy/`, `sprints/`, `docs/` (antigos)
- ✅ Removido: Todos os `.md` da raiz
- ✅ Mantido: `LGPD/` (intacto)

#### 1.2 Reestruturação de Código
- ✅ `shared_kernel/` → `shared/`
- ✅ Módulos movidos para `src/modules/`:
  - `admin/` (Django - Gestão de usuários)
  - `cidades/` (Django - Multi-tenancy)
  - `streaming/` (FastAPI - Vídeo)
- ✅ Criados novos módulos:
  - `cameras/` (FastAPI - Hardware)
  - `deteccoes/` (FastAPI - Eventos IA)

#### 1.3 Infraestrutura
- ✅ `docker-compose.yml` simplificado:
  - Removido: Kong, HAProxy, Elasticsearch, Logstash, Kibana
  - Mantido: PostgreSQL, Redis, RabbitMQ, MinIO, MediaMTX, Prometheus, Grafana
  - Adicionado: Nginx como gateway único
- ✅ `docker/nginx/nginx.conf`:
  - Roteamento: `/api/v1/` → FastAPI, `/admin/` → Django
  - Proxy HLS: `/stream/` → MediaMTX:8888
  - CORS configurado globalmente
  - WebSockets: `/ws/` → FastAPI
- ✅ `docker/nginx/Dockerfile` criado
- ✅ `mediamtx.yml` restaurado (versão otimizada original):
  - HLS: fmp4, 2s segments, 10 count
  - API v3 habilitada (:9997)
  - Autenticação configurada
  - Paths dinâmicos via API

#### 1.4 Documentação
- ✅ `README.md` atualizado:
  - Quick start
  - Arquitetura simplificada
  - Endpoints do gateway
  - Estratégia de IA (Plug & Play)
- ✅ `docs/prompt_engineering/context.md` criado:
  - Decisões arquiteturais
  - Bounded contexts
  - Fluxos críticos
  - Modelo de dados
  - Roadmap completo

### Estrutura Final
```
vms-v2/
├── docker-compose.yml          # Simplificado (9 serviços)
├── mediamtx.yml                # HLS otimizado
├── README.md                   # Nova documentação
├── LGPD/                       # Mantido intacto
├── docs/
│   └── prompt_engineering/
│       ├── context.md          # Cérebro do projeto
│       └── FASES.md            # Este arquivo
├── docker/
│   ├── nginx/
│   │   ├── Dockerfile
│   │   └── nginx.conf          # Gateway único
│   ├── postgres/
│   ├── backend/
│   └── streaming/
└── src/
    ├── shared/                 # Ex-shared_kernel
    │   ├── domain/
    │   ├── application/
    │   └── infrastructure/
    └── modules/
        ├── admin/              # Django - Usuários
        ├── cidades/            # Django - Tenants
        ├── streaming/          # FastAPI - Vídeo
        ├── cameras/            # FastAPI - Hardware (novo)
        └── deteccoes/          # FastAPI - IA (novo)
```

---

## 🚧 FASE 2: Hardware & Smart URLs (PRÓXIMA)

### Objetivos
- Implementar Smart URL Builder (Strategy Pattern)
- Refatorar MediaMTX Client para API v3
- Criar endpoint de Webhooks LPR
- Implementar Camera Health Check

### Tarefas

#### 2.1 Smart URL Builder
**Arquivo**: `src/modules/cameras/domain/services/url_builder.py`

Implementar:
- Interface `UrlBuilder` (ABC)
- `IntelbrasUrlBuilder` (Strategy)
- `HikvisionUrlBuilder` (Strategy)
- `UrlBuilderFactory` (Factory)

**Exemplo de uso**:
```python
builder = UrlBuilderFactory.get_builder("intelbras")
url = builder.build(ip="192.168.1.100", user="admin", password="123")
# Output: rtsp://admin:123@192.168.1.100:554/cam/realmonitor?channel=1&subtype=0
```

#### 2.2 MediaMTX Client (API v3)
**Arquivo**: `src/modules/streaming/domain/services/mediamtx_client.py`

Refatorar para usar API v3:
- `POST /v3/config/paths/add` - Criar path
- `DELETE /v3/config/paths/remove/{name}` - Remover path
- `GET /v3/config/paths/list` - Listar paths
- `PATCH /v3/config/paths/patch/{name}` - Atualizar path

**Configuração de path**:
```json
{
  "name": "cam01_live",
  "source": "rtsp://admin:123@192.168.1.100:554/cam/realmonitor?channel=1&subtype=0",
  "sourceOnDemand": true,
  "record": false
}
```

#### 2.3 Webhook LPR
**Arquivo**: `src/modules/cameras/infra/webhooks.py`

Endpoint: `POST /api/v1/webhooks/lpr`

Payload esperado:
```json
{
  "camera_id": "cam01",
  "placa": "ABC1D23",
  "timestamp": "2024-01-15T10:30:00Z",
  "confianca": 0.95,
  "imagem_url": "https://...",
  "signature": "hmac-sha256..."
}
```

Fluxo:
1. Validar assinatura HMAC
2. Buscar câmera no banco
3. Enriquecer dados (tenant_id, localização)
4. Publicar no RabbitMQ (`deteccoes.lpr`)
5. Retornar 202 Accepted

#### 2.4 Camera Health Check
**Arquivo**: `src/modules/cameras/domain/services/health_service.py`

Implementar:
- Testar conectividade RTSP (timeout 5s)
- Verificar se MediaMTX consegue conectar
- Atualizar status no banco (online/offline)
- Worker periódico (a cada 60s)

---

## 🎨 FASE 3: Visualização HLS (1 semana)

### Objetivos
- Ajuste fino do MediaMTX
- Endpoint de mosaicos
- Player HLS otimizado

### Tarefas

#### 3.1 Endpoint de Mosaicos
**Arquivo**: `src/modules/streaming/infrastructure/web/mosaic_routes.py`

- `POST /api/v1/mosaics` - Criar mosaico
- `GET /api/v1/mosaics/{id}` - Obter mosaico
- `PATCH /api/v1/mosaics/{id}` - Atualizar layout
- `DELETE /api/v1/mosaicos/{id}` - Remover

**Payload**:
```json
{
  "nome": "Mosaico Centro",
  "layout": "2x2",
  "cameras": ["cam01", "cam02", "cam03", "cam04"]
}
```

#### 3.2 Thumbnails e Timeline
- Gerar thumbnails a cada 10s (FFmpeg)
- Endpoint: `GET /api/v1/cameras/{id}/timeline?start=...&end=...`
- Armazenar no MinIO

---

## 🔒 FASE 4: Storage & LGPD (3 dias)

### Objetivos
- Worker de limpeza automática
- Políticas de retenção por tenant
- Logs de auditoria

### Tarefas

#### 4.1 Cleanup Worker
**Arquivo**: `src/modules/streaming/infrastructure/workers/cleanup_service.py`

- Executar diariamente (Celery Beat)
- Aplicar política de retenção do plano
- Deletar gravações antigas do MinIO
- Anonimizar dados de detecções antigas
- Registrar em log de auditoria

#### 4.2 Logs de Auditoria
**Tabela**: `audit_logs`

Registrar:
- Acesso a vídeos
- Download de gravações
- Criação/exclusão de câmeras
- Alteração de permissões

---

## ⚡ FASE 5: Tempo Real (3 dias)

### Objetivos
- WebSockets para alertas
- Notificações push
- Dashboard em tempo real

### Tarefas

#### 5.1 WebSocket Server
**Arquivo**: `src/modules/streaming/infrastructure/web/websocket_routes.py`

- Endpoint: `ws://localhost/ws/alerts`
- Autenticação via JWT no query string
- Filtro por tenant_id
- Enviar eventos de detecção em tempo real

#### 5.2 Dashboard Metrics
- Câmeras online/offline
- Viewers simultâneos
- Storage usado
- Detecções nas últimas 24h

---

## 🤖 FASE 6: IA Própria (Futuro - Não implementar agora)

### Objetivos
- Container YOLO para detecção
- OCR para placas
- Análise de comportamento

### Arquitetura Preparada
- MediaMTX: Paths duplicados (`cam01_live` + `cam01_ai`)
- RabbitMQ: Exchange `deteccoes.events` pronto
- Webhook: Endpoint `/api/v1/webhooks/lpr` aceita eventos

### Container de IA (Futuro)
```yaml
ai-processor:
  image: gtvision/ai-processor:latest
  environment:
    MEDIAMTX_URL: rtsp://mediamtx:8554
    RABBITMQ_URL: amqp://gtvision:password@rabbitmq:5672
  depends_on:
    - mediamtx
    - rabbitmq
```

**Fluxo**:
1. Consome RTSP do MediaMTX
2. Processa frames com YOLO
3. Extrai placas com OCR
4. Publica eventos no RabbitMQ
5. Worker `deteccoes` persiste no PostgreSQL

---

## 📊 Métricas de Sucesso

FASE 1: Fundação & Limpeza ✅
- [x] Infraestrutura: Remoção de Kong/HAProxy e adoção de     Nginx Unificado.
- [x] Arquitetura: Estrutura de pastas DDD Refatorada (src/modules).
- [x] Documentação: Contexto de Engenharia de Prompt criado.

FASE 2: Domínio de Hardware (UX & Ingestão) ✅
- [x] Cadastro Rápido: Lógica de UrlBuilder (Strategy Pattern) definida.
  [x] Automação: Provisionamento dinâmico na API v3 do MediaMTX.
  [x] Ingestão: Endpoint de Webhook LPR (Intelbras/Hikvision) desenhado.
  [x] Diagnóstico: Health Check básico das câmeras.

FASE 3: Streaming Robusto (A Experiência do Usuário) ✅
Foco: Zero "Tela Preta" e Baixa Latência.

- [x] Tuning HLS: Latência < 8s (Configuração híbrida mediamtx.yml).
- [x] Resiliência: Player Frontend com Auto-Recover (Reinicia em caso de 404/Erro de Rede).
- [x] Mosaicos: Backend para Grid 2x2 e 4x4 (Agregação de Streams).
- [x] Thumbnails: Geração via Worker (evita onerar o stream principal).
- [x] Snapshot Sob Demanda: Endpoint API para capturar foto atual (sem carregar vídeo).
- [x] Segurança: Proteção de rota de vídeo (Nginx auth_request valida Token).
- [x] Fallback Visual: Placeholder "Sinal Perdido" se o HLS falhar.

FASE 4: Gestão de Dados & Ciclo de Vida (Proteção Legal) ✅
Foco: Evitar Crash de Disco e Garantir Auditoria.
- [x] Cleanup Inteligente: Worker de expurgo que respeita Flags de Incidentes (LGPD).
- [x] Evidências: Exportação de Clipe MP4 (Stitching de segmentos .ts).
- [x] Circuit Breaker: Bloqueio de gravação se Disco > 95% (Proteção de Infra).
- [x] Integridade (Sanity Check): Job noturno que detecta arquivos órfãos (Disco vs Banco).
- [x] Auditoria: Relatório PDF de Expurgo Automático (Comprovação Jurídica).

FASE 5: Operação Real-Time (Sala de Guerra) ✅
Foco: Consciência Situacional Imediata.
- [x] Alertas LPR: WebSocket (< 500ms) enviando detecção com recorte da placa.
- [x] Mapa Tático: Plotagem de câmeras em mapa (GeoJSON).
- [x] Dashboard de Saúde: Monitoramento em tempo real (Online/Offline/Falha de Gravação).
- [x] Observabilidade: Alerta para Admin se filas do RabbitMQ engargalarem.
- [x] Notificações: Push Notification para App/Navegador do Gestor.

  ---

## 🎯 Próximos Passos

**Agora**: Iniciar FASE 2 - Smart URL Builder

**Comando para começar**:
```bash
# Criar branch
git checkout -b feature/fase-2-hardware

# Iniciar implementação
# 1. url_builder.py
# 2. mediamtx_client.py (refactor)
# 3. webhooks.py
# 4. health_service.py
```

---

**Última atualização**: FASE 1 concluída
**Próxima fase**: FASE 2 - Hardware & Smart URLs
**Prazo total**: 2 semanas (10 dias úteis)
