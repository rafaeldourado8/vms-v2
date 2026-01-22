# GT-Vision VMS - Context Document

## 🎯 Visão Geral

Sistema VMS (Video Management System) Enterprise para Prefeituras brasileiras com foco em:
- **Escalabilidade**: Multi-tenant (1 cidade = 1 tenant)
- **Conformidade**: LGPD by design
- **Performance**: HLS com latência ~6-8s
- **Modularidade**: Arquitetura DDD com Bounded Contexts

## 🏛️ Decisões Arquiteturais

### 1. Gateway Único (Nginx)
**Decisão**: Remover Kong/HAProxy, usar apenas Nginx.

**Razão**: 
- Simplicidade operacional
- Menor overhead
- CORS nativo
- Suficiente para escala inicial (até 1000 câmeras)

**Trade-off**: Menos features enterprise (rate limiting avançado, plugins). Aceitável para MVP.

### 2. HLS First (MediaMTX)
**Decisão**: Priorizar HLS sobre WebRTC.

**Razão**:
- Compatibilidade universal (todos os browsers)
- Estabilidade comprovada
- Latência aceitável (6-8s) para vigilância urbana
- Menor complexidade de infraestrutura

**Configuração Crítica**:
```yaml
hlsVariant: fmp4          # Melhor qualidade
hlsSegmentDuration: 2s    # Latência vs estabilidade
hlsSegmentCount: 7        # Buffer de 14s
```

### 3. IA Plug & Play
**Decisão**: Não implementar YOLO agora. Preparar arquitetura.

**Fase Atual**: Webhooks de câmeras com LPR nativo (Intelbras/Hikvision).

**Fase Futura**: Container de IA separado que:
1. Consome RTSP do MediaMTX
2. Processa com YOLO/OCR
3. Publica eventos no RabbitMQ
4. Worker `deteccoes` persiste no PostgreSQL

**Pontos de Integração Preparados**:
- MediaMTX API v3 para criar paths dinâmicos
- RabbitMQ exchange `deteccoes.events`
- Webhook endpoint `/api/v1/webhooks/lpr`

### 4. Smart URL Builder
**Decisão**: Gerar URLs RTSP automaticamente a partir de IP + Marca.

**Implementação**: Strategy Pattern
```python
# cameras/domain/services/url_builder.py
class UrlBuilderFactory:
    @staticmethod
    def get_builder(marca: str) -> UrlBuilder:
        if marca == "intelbras":
            return IntelbrasUrlBuilder()
        elif marca == "hikvision":
            return HikvisionUrlBuilder()
```

**Exemplo**:
```
Input: IP=192.168.1.100, Marca=intelbras, User=admin, Pass=123
Output: rtsp://admin:123@192.168.1.100:554/cam/realmonitor?channel=1&subtype=0
```

## 📦 Bounded Contexts

### Admin (Django)
**Responsabilidade**: Gestão de usuários, roles, permissões.

**Agregados**: User, Role, Permission

**Infraestrutura**: Django ORM, Django Admin UI

### Cidades (Django)
**Responsabilidade**: Multi-tenancy, planos, limites.

**Agregados**: Cidade (Tenant), Plano, UsuarioCidade

**Regras de Negócio**:
- 1 Cidade = 1 Tenant isolado
- Plano define limite de câmeras
- Middleware injeta `X-Tenant-ID` em todas as queries

### Cameras (FastAPI)
**Responsabilidade**: Cadastro, configuração, health check.

**Entidades**: Camera, Fabricante, Modelo

**Serviços**:
- `UrlBuilderFactory`: Gera URLs RTSP
- `CameraHealthService`: Testa conectividade
- `MediaMTXClient`: Cria paths no MediaMTX via API v3

### Streaming (FastAPI)
**Responsabilidade**: Vídeo ao vivo, gravações, mosaicos.

**Entidades**: Stream, Recording, Mosaic, Clip

**Serviços**:
- `MediaMTXClient`: Gerencia paths HLS
- `FFmpegService`: Transcodificação, thumbnails
- `StorageService`: Upload para MinIO
- `CleanupWorker`: Aplica políticas de retenção LGPD

### Deteccoes (FastAPI)
**Responsabilidade**: Eventos de IA, alertas, webhooks.

**Entidades**: Deteccao, Alerta, Webhook

**Fluxo**:
1. Webhook recebe evento (câmera ou IA)
2. Valida e enriquece dados
3. Publica no RabbitMQ
4. Consumer persiste no PostgreSQL
5. WebSocket notifica frontend

## 🔐 Segurança

### Autenticação
- JWT (SimpleJWT para Django, python-jose para FastAPI)
- Refresh tokens com rotação
- Blacklist em Redis

### Autorização
- RBAC (Role-Based Access Control)
- Roles: `superadmin`, `admin_cidade`, `operador`, `visualizador`
- Permissions granulares por recurso

### Tenant Isolation
```python
# Middleware injeta tenant_id em todas as queries
class TenantMiddleware:
    def __call__(self, request):
        tenant_id = request.headers.get("X-Tenant-ID")
        # Valida e injeta no contexto
```

## 📊 Observabilidade

### Métricas (Prometheus)
- `camera_status{tenant, camera_id}`: Online/Offline
- `stream_viewers{tenant, camera_id}`: Viewers simultâneos
- `recording_size_bytes{tenant}`: Storage por tenant
- `deteccao_count{tenant, tipo}`: Eventos de IA

### Logs (Estruturados)
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "tenant_id": "cidade-sp",
  "user_id": "user123",
  "action": "camera.created",
  "camera_id": "cam01",
  "ip": "192.168.1.100"
}
```

### Alertas
- Camera offline > 5min
- Storage > 80% do limite do plano
- Falha de gravação
- Detecção de anomalia (IA)

## 🗄️ Modelo de Dados

### Cameras
```sql
CREATE TABLE cameras (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(50) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    ip INET NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(100),
    rtsp_url TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'offline',
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(tenant_id, ip)
);
```

### Deteccoes
```sql
CREATE TABLE deteccoes (
    id UUID PRIMARY KEY,
    tenant_id VARCHAR(50) NOT NULL,
    camera_id UUID REFERENCES cameras(id),
    tipo VARCHAR(50) NOT NULL, -- 'lpr', 'pessoa', 'veiculo'
    dados JSONB NOT NULL,      -- Flexível para diferentes tipos
    confianca FLOAT,
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_deteccoes_tenant_timestamp ON deteccoes(tenant_id, timestamp DESC);
CREATE INDEX idx_deteccoes_tipo ON deteccoes(tipo);
```

## 🔄 Fluxos Críticos

### 1. Cadastro de Câmera
```
1. POST /api/v1/cameras {ip, marca, usuario, senha}
2. UrlBuilderFactory gera rtsp_url
3. CameraHealthService testa conectividade
4. MediaMTXClient cria path no MediaMTX (POST /v3/config/paths/add)
5. Persiste no PostgreSQL
6. Publica evento camera.created no RabbitMQ
7. Retorna {id, rtsp_url, hls_url}
```

### 2. Streaming HLS
```
1. Frontend solicita /stream/cam01_live/index.m3u8
2. Nginx proxy para MediaMTX:8888
3. MediaMTX:
   - Se path existe: retorna playlist
   - Se não existe: retorna 404 (criar via API primeiro)
4. Frontend usa hls.js para reproduzir
```

### 3. Detecção LPR (Webhook)
```
1. Câmera envia POST /api/v1/webhooks/lpr
2. Valida assinatura (HMAC)
3. Enriquece com dados da câmera
4. Publica no RabbitMQ exchange 'deteccoes.events'
5. Consumer persiste no PostgreSQL
6. WebSocket notifica frontend em tempo real
7. Se placa em lista de alerta: dispara notificação
```

## 🚧 Roadmap

### Fase 1: Fundação (2 semanas) ✅
- [x] Limpeza de infraestrutura obsoleta
- [x] Nginx como gateway único
- [x] MediaMTX configurado para HLS
- [x] Documentação atualizada

### Fase 2: Hardware (1 semana)
- [ ] Smart URL Builder (Strategy Pattern)
- [ ] MediaMTX Client (API v3)
- [ ] Webhook LPR (Intelbras/Hikvision)
- [ ] Camera Health Check

### Fase 3: Visualização (1 semana)
- [ ] Endpoint de mosaicos
- [ ] Player HLS otimizado
- [ ] Thumbnails e timeline

### Fase 4: Storage & LGPD (3 dias)
- [ ] Worker de limpeza automática
- [ ] Políticas de retenção por tenant
- [ ] Logs de auditoria

### Fase 5: Tempo Real (3 dias)
- [ ] WebSockets para alertas
- [ ] Notificações push
- [ ] Dashboard em tempo real

### Fase 6: IA Própria (Futuro)
- [ ] Container YOLO
- [ ] OCR para placas
- [ ] Detecção de pessoas/veículos
- [ ] Análise de comportamento

## 🎓 Convenções de Código

### Nomenclatura
- **Agregados**: PascalCase (User, Cidade, Camera)
- **Entidades**: PascalCase (Role, Permission, Stream)
- **Value Objects**: PascalCase (Email, CNPJ, StatusCamera)
- **Use Cases**: snake_case (create_user, start_stream)
- **DTOs**: PascalCase + Suffix (CreateUserDTO, CameraResponseDTO)

### Estrutura de Arquivos
```
module/
├── domain/
│   ├── aggregates/      # Raízes de agregado
│   ├── entities/        # Entidades
│   ├── value_objects/   # Objetos de valor
│   ├── repositories/    # Interfaces
│   ├── services/        # Serviços de domínio
│   └── events/          # Eventos de domínio
├── application/
│   ├── use_cases/       # Casos de uso
│   ├── dtos/            # Data Transfer Objects
│   └── event_handlers/  # Handlers de eventos
└── infrastructure/
    ├── persistence/     # Implementações de repositórios
    ├── web/             # Controllers/Routes
    └── messaging/       # RabbitMQ consumers
```

### Testes
- **Unit**: Domínio puro, sem I/O
- **Integration**: Repositórios, APIs externas
- **E2E**: Fluxos completos via HTTP

## 📞 Contatos Técnicos

- **Arquiteto**: [Definir]
- **Tech Lead**: [Definir]
- **DevOps**: [Definir]

## 📚 Referências

- [MediaMTX Docs](https://github.com/bluenviron/mediamtx)
- [HLS Spec](https://datatracker.ietf.org/doc/html/rfc8216)
- [DDD by Eric Evans](https://www.domainlanguage.com/ddd/)
- [LGPD](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
