# GT-Vision VMS

Sistema VMS (Video Management System) enterprise para prefeituras brasileiras.

## 🏗️ Arquitetura

- **Padrão**: Domain-Driven Design (DDD)
- **Princípios**: SOLID
- **Estilo**: Monolito Modular
- **Bounded Contexts**: Admin, Cidades, Streaming, AI

## 🛠️ Stack Tecnológica

- **Backend**: Django 5.0 + FastAPI
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Message Broker**: RabbitMQ 3
- **Streaming**: MediaMTX
- **Proxy**: HAProxy + Kong
- **Observabilidade**: Prometheus + Grafana + ELK
- **Deploy**: Docker Compose + Terraform (AWS)

## 📋 Requisitos

- Docker Desktop
- Python 3.11+
- Poetry

## 🚀 Quick Start

### Sprint 11 - Integração Real (ATUAL)

```bash
# 1. Iniciar infraestrutura (PostgreSQL, Redis, RabbitMQ, MinIO, MediaMTX)
scripts\sprint11-setup.bat

# 2. Instalar dependências
poetry install

# 3. Aplicar migrations
poetry run python manage.py migrate

# 4. Iniciar Django (Admin + Cidades)
poetry run python manage.py runserver

# 5. Iniciar FastAPI (Streaming + AI) - em outro terminal
cd src/streaming
poetry run uvicorn infrastructure.web.main:app --reload --port 8001
```

### Setup Anterior (Sprints 0-10)

```bash
# Clone o repositório
git clone <repo-url>
cd GT-Vision-VMS

# Execute o setup
scripts\setup.bat
```

### 2. Configuração

Edite o arquivo `.env` com suas configurações.

### 3. Iniciar Serviços

```bash
# Todos os serviços
docker-compose up -d

# Apenas infraestrutura (dev)
docker-compose -f docker-compose.dev.yml up -d
```

### 4. Acessar

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **Streaming API**: http://localhost:8001
- **Grafana**: http://localhost:3000 (admin/admin)
- **Kibana**: http://localhost:5601
- **RabbitMQ**: http://localhost:15672 (gtvision/gtvision_password)
- **HAProxy Stats**: http://localhost:8404/stats

## 🧪 Testes

```bash
# Executar todos os testes
scripts\test.bat

# Apenas unitários
poetry run pytest -m unit

# Apenas integração
poetry run pytest -m integration

# Com cobertura
poetry run pytest --cov=src --cov-report=html
```

## 🔍 Code Quality

```bash
# Executar todas as verificações
scripts\lint.bat

# Formatação
poetry run black src/
poetry run isort src/

# Linting
poetry run flake8 src/

# Type checking
poetry run mypy src/

# Security
poetry run bandit -r src/
```

## 📁 Estrutura do Projeto

```
GT-Vision-VMS/
├── src/
│   ├── shared_kernel/      # Shared Kernel (DDD)
│   ├── admin/              # Admin Context
│   ├── cidades/            # Cidades Context
│   ├── streaming/          # Streaming Context
│   └── ai/                 # AI Context
├── docker/                 # Dockerfiles
├── haproxy/               # HAProxy config
├── kong/                  # Kong config
├── monitoring/            # Prometheus + Logstash
├── scripts/               # Automation scripts
├── sprints/               # Sprint planning
├── .context/              # Project context
└── docker-compose.yml     # Docker Compose
```

## 📚 Documentação

### Sprint 11 (Atual)
- [Quick Start Sprint 11](sprints/sprint-11-quickstart.md) - Começar agora
- [Sprint 11 README](sprints/sprint-11.md) - Documentação completa
- [Sprint 11 Checklist](sprints/sprint-11-checklist.md) - Progresso detalhado
- [Sprint 11 Architecture](sprints/sprint-11-architecture.md) - Arquitetura de integração
- [Integration Guide](sprints/sprint-11-integration-guide.md) - Guia técnico

### Contexto do Projeto
- [Contexto do Projeto](.context/PROJECT_CONTEXT.md)
- [Estado Atual](.context/CURRENT_STATE.md)
- [Planejamento de Sprints](sprints/README.md)
- [Sprint Atual](sprints/sprint-11.md)

## 🔒 Segurança

- OWASP Top 10 compliance
- LGPD compliance
- Rate limiting
- JWT authentication
- Input validation
- SQL injection prevention

## 📊 Métricas de Qualidade

- Cobertura de testes: >90%
- Complexidade ciclomática: <10
- Maintainability Index: >70

## 🤝 Contribuindo

1. Leia `.context/PROJECT_CONTEXT.md`
2. Siga a arquitetura DDD
3. Mantenha cobertura >90%
4. Execute `scripts\lint.bat` antes de commit
5. Atualize `.context/CURRENT_STATE.md`

## 📝 License

Proprietary - GT-Vision Team

## 📞 Suporte

Para dúvidas, consulte:
1. `.context/PROJECT_CONTEXT.md`
2. `sprints/README.md`
3. Sprint atual em `sprints/sprint-X.md`
