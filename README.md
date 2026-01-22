# GT-Vision VMS v2

Sistema de Gerenciamento de Vídeo (VMS) Enterprise para Prefeituras com arquitetura DDD e conformidade LGPD.

## 🏗️ Arquitetura

### Stack Tecnológico
- **Backend Admin**: Django 5.0 + DRF (Gestão/Backoffice)
- **Backend Streaming**: FastAPI (Alta Performance/Tempo Real)
- **Gateway**: Nginx (Roteamento Unificado)
- **Streaming**: MediaMTX (HLS/RTSP/RTMP)
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Message Broker**: RabbitMQ 3
- **Storage**: MinIO (S3-compatible)
- **Observability**: Prometheus + Grafana

### Estrutura de Módulos (DDD)
```
src/
├── shared/              # Kernel compartilhado
│   ├── domain/          # Interfaces base (Entity, AggregateRoot, Repository)
│   ├── infra/           # Redis, RabbitMQ, PostgreSQL
│   └── security/        # Auth, RBAC, Tenant Isolation
│
└── modules/             # Bounded Contexts
    ├── admin/           # Gestão de usuários e permissões
    ├── cidades/         # Multi-tenancy (Prefeituras)
    ├── cameras/         # Hardware e Smart URLs
    ├── streaming/       # Vídeo ao vivo e gravações
    └── deteccoes/       # Eventos e alertas (LPR, IA)
```

## 🚀 Quick Start

### Pré-requisitos
- Docker 24+ e Docker Compose
- Python 3.10+
- Poetry 1.7+

### Instalação

1. **Clone e configure**
```bash
git clone <repo>
cd vms-v2
cp .env.example .env
```

2. **Inicie a infraestrutura**
```bash
docker-compose up -d postgres redis rabbitmq minio mediamtx
```

3. **Instale dependências**
```bash
poetry install
```

4. **Migrations**
```bash
poetry run python manage.py migrate
```

5. **Inicie os serviços**
```bash
# Terminal 1 - Django Admin
poetry run python manage.py runserver 8000

# Terminal 2 - FastAPI Streaming
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload

# Terminal 3 - Nginx
docker-compose up nginx
```

## 📡 Endpoints

### Gateway Nginx (Porta 80)
- `GET /health` - Health check
- `/admin/` - Django Admin UI
- `/api/admin/*` - Django REST API
- `/api/v1/*` - FastAPI (Streaming/Câmeras)
- `/ws/*` - WebSockets
- `/stream/*` - HLS Streaming (MediaMTX)

### Exemplos

**Criar câmera com Smart URL**
```bash
curl -X POST http://localhost/api/v1/cameras \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: cidade-sp" \
  -d '{
    "ip": "192.168.1.100",
    "marca": "intelbras",
    "modelo": "VIP 1220 B",
    "usuario": "admin",
    "senha": "admin123"
  }'
```

**Assistir stream HLS**
```bash
# URL gerada automaticamente
http://localhost/stream/cam01_live/index.m3u8
```

## 🎯 Estratégia de IA (Plug & Play)

### Fase Atual: Webhooks Nativos
Câmeras Intelbras/Hikvision com LPR embarcado enviam eventos via HTTP POST:
```
POST /api/v1/webhooks/lpr
{
  "camera_id": "cam01",
  "placa": "ABC1D23",
  "timestamp": "2024-01-15T10:30:00Z",
  "confianca": 0.95
}
```

### Fase Futura: IA Própria (YOLO)
Arquitetura preparada para container de IA:
- MediaMTX cria paths duplicados (`cam01_live` + `cam01_ai`)
- Container de IA consome RTSP, processa e publica no RabbitMQ
- Worker `deteccoes` consome eventos e armazena

## 🔒 Conformidade LGPD

Consulte `LGPD/` para:
- Políticas de retenção
- Anonimização de dados
- Logs de auditoria
- Direitos do titular

## 📊 Observabilidade

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **RabbitMQ Management**: http://localhost:15672 (gtvision/gtvision_password)
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin)

## 🧪 Testes

```bash
# Unit tests
poetry run pytest src/ -m unit

# Integration tests
poetry run pytest src/ -m integration

# Coverage
poetry run pytest --cov=src --cov-report=html
```

## 📝 Desenvolvimento

### Code Quality
```bash
# Format
poetry run black src/
poetry run isort src/

# Lint
poetry run flake8 src/
poetry run mypy src/

# Security
poetry run bandit -r src/
```

### Pre-commit
```bash
poetry run pre-commit install
poetry run pre-commit run --all-files
```

## 📚 Documentação Adicional

- [Context.md](docs/prompt_engineering/context.md) - Contexto completo do projeto
- [LGPD](LGPD/) - Conformidade e políticas

## 🤝 Contribuindo

1. Siga a arquitetura DDD estabelecida
2. Mantenha cobertura de testes > 80%
3. Use conventional commits
4. Documente decisões arquiteturais

## 📄 Licença

Proprietário - GT-Vision Team
