# SPRINT 0: Fundação e Arquitetura (5 dias)

## 🎯 Objetivo
Estabelecer base sólida DDD, estrutura de pastas, configurações iniciais e ferramentas de qualidade.

---

## 📋 Checklist de Entregáveis

### Dia 1: Estrutura DDD e Shared Kernel
- [ ] Criar estrutura de pastas DDD para todos os bounded contexts
- [ ] Implementar Shared Kernel (base classes)
- [ ] Configurar pyproject.toml com dependências
- [ ] Configurar .env.example

### Dia 2: Docker Compose e Infraestrutura
- [ ] Docker Compose completo (PostgreSQL, Redis, RabbitMQ, MediaMTX)
- [ ] Configurar networks e volumes
- [ ] Scripts de inicialização de banco
- [ ] Health checks para todos os serviços

### Dia 3: Setup de Testes e Qualidade
- [ ] Configurar pytest + pytest-cov
- [ ] Configurar mutation testing (mutmut)
- [ ] Configurar pre-commit hooks
- [ ] Configurar black, flake8, mypy, isort, bandit

### Dia 4: Documentação e ADRs
- [ ] Criar template de ADR
- [ ] ADR 001: Escolha de arquitetura (DDD + Monolito Modular)
- [ ] ADR 002: Escolha de tecnologias
- [ ] Diagrama C4 - Contexto e Containers

### Dia 5: Validação e Testes
- [ ] Testar build do Docker Compose
- [ ] Validar conexões entre serviços
- [ ] Executar testes de exemplo
- [ ] Documentar setup para desenvolvedores

---

## 🏗️ Estrutura de Pastas Final

```
GT-Vision-VMS/
├── src/
│   ├── shared_kernel/
│   │   ├── __init__.py
│   │   ├── domain/
│   │   │   ├── __init__.py
│   │   │   ├── aggregate_root.py
│   │   │   ├── entity.py
│   │   │   ├── value_object.py
│   │   │   ├── domain_event.py
│   │   │   ├── domain_exception.py
│   │   │   └── repository.py (interface)
│   │   ├── application/
│   │   │   ├── __init__.py
│   │   │   ├── use_case.py (base)
│   │   │   ├── event_bus.py
│   │   │   └── dto.py (base)
│   │   └── infrastructure/
│   │       ├── __init__.py
│   │       ├── database.py
│   │       ├── cache.py
│   │       ├── message_broker.py
│   │       └── logger.py
│   │
│   ├── admin/
│   │   ├── __init__.py
│   │   ├── domain/
│   │   │   ├── aggregates/
│   │   │   ├── entities/
│   │   │   ├── value_objects/
│   │   │   ├── events/
│   │   │   ├── repositories/
│   │   │   └── services/
│   │   ├── application/
│   │   │   ├── use_cases/
│   │   │   ├── dtos/
│   │   │   ├── event_handlers/
│   │   │   └── services/
│   │   ├── infrastructure/
│   │   │   ├── persistence/
│   │   │   ├── messaging/
│   │   │   └── web/
│   │   │       └── django_app/
│   │   └── tests/
│   │       ├── unit/
│   │       ├── integration/
│   │       └── e2e/
│   │
│   ├── cidades/
│   │   ├── __init__.py
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   └── tests/
│   │
│   ├── streaming/
│   │   ├── __init__.py
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   │   └── web/
│   │   │       └── fastapi_app/
│   │   └── tests/
│   │
│   └── ai/
│       ├── __init__.py
│       ├── domain/
│       ├── application/
│       ├── infrastructure/
│       └── tests/
│
├── docker/
│   ├── backend/
│   │   └── Dockerfile
│   ├── streaming/
│   │   └── Dockerfile
│   ├── nginx/
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   └── postgres/
│       └── init.sql
│
├── haproxy/
│   └── haproxy.cfg
│
├── kong/
│   └── kong.yml
│
├── mediamtx.yml
│
├── docker-compose.yml
├── docker-compose.dev.yml
├── docker-compose.prod.yml
│
├── pyproject.toml
├── poetry.lock
├── requirements.txt
├── requirements-dev.txt
│
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── pytest.ini
├── mypy.ini
├── .flake8
│
├── docs/
│   ├── architecture/
│   │   ├── adr/
│   │   │   ├── 001-ddd-architecture.md
│   │   │   └── 002-technology-choices.md
│   │   ├── diagrams/
│   │   │   ├── c4-context.puml
│   │   │   └── c4-containers.puml
│   │   └── README.md
│   ├── api/
│   └── development/
│       └── setup.md
│
├── scripts/
│   ├── setup.sh
│   ├── test.sh
│   ├── lint.sh
│   └── deploy.sh
│
├── terraform/
│   ├── modules/
│   └── environments/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
├── sprints/
│   ├── README.md
│   ├── sprint-0.md
│   └── ...
│
└── README.md
```

---

## 🐳 Docker Compose Services

### Services:
1. **postgres** - PostgreSQL 15
2. **redis** - Redis 7
3. **rabbitmq** - RabbitMQ 3 (management)
4. **mediamtx** - MediaMTX (streaming)
5. **backend** - Django (Admin + Cidades)
6. **streaming** - FastAPI (Streaming + AI)
7. **nginx** - Nginx (static files)
8. **haproxy** - HAProxy (load balancer)
9. **kong** - Kong Gateway
10. **prometheus** - Prometheus
11. **grafana** - Grafana
12. **elasticsearch** - Elasticsearch
13. **logstash** - Logstash
14. **kibana** - Kibana

---

## 📦 Dependências Principais

### Backend (Django)
```toml
[tool.poetry.dependencies]
python = "^3.11"
django = "^5.0"
djangorestframework = "^3.14"
djangorestframework-simplejwt = "^5.3"
psycopg2-binary = "^2.9"
redis = "^5.0"
celery = "^5.3"
pika = "^1.3"
pydantic = "^2.5"
python-decouple = "^3.8"
```

### Streaming (FastAPI)
```toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.109"
uvicorn = {extras = ["standard"], version = "^0.27"}
pydantic = "^2.5"
sqlalchemy = "^2.0"
asyncpg = "^0.29"
redis = "^5.0"
aio-pika = "^9.3"
httpx = "^0.26"
websockets = "^12.0"
ffmpeg-python = "^0.2"
```

### Dev Dependencies
```toml
[tool.poetry.group.dev.dependencies]
pytest = "^7.4"
pytest-cov = "^4.1"
pytest-asyncio = "^0.23"
pytest-django = "^4.7"
black = "^24.1"
flake8 = "^7.0"
mypy = "^1.8"
isort = "^5.13"
bandit = "^1.7"
pre-commit = "^3.6"
mutmut = "^2.4"
locust = "^2.20"
faker = "^22.0"
```

---

## ⚙️ Configurações de Qualidade

### pytest.ini
```ini
[pytest]
DJANGO_SETTINGS_MODULE = admin.infrastructure.web.django_app.settings
python_files = tests.py test_*.py *_tests.py
testpaths = src
addopts = 
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=90
    --strict-markers
    --tb=short
```

### .flake8
```ini
[flake8]
max-line-length = 100
exclude = .git,__pycache__,migrations,venv
max-complexity = 10
ignore = E203,W503
```

### mypy.ini
```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
plugins = pydantic.mypy
```

### .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.6
    hooks:
      - id: bandit
        args: ['-c', 'pyproject.toml']
```

---

## 📝 ADR Template

```markdown
# ADR XXX: [Título]

## Status
[Proposto | Aceito | Rejeitado | Depreciado | Substituído por ADR-YYY]

## Contexto
[Descreva o contexto e o problema que precisa ser resolvido]

## Decisão
[Descreva a decisão tomada]

## Consequências
### Positivas
- [Consequência positiva 1]
- [Consequência positiva 2]

### Negativas
- [Consequência negativa 1]
- [Consequência negativa 2]

## Alternativas Consideradas
1. [Alternativa 1]
2. [Alternativa 2]

## Referências
- [Link 1]
- [Link 2]
```

---

## 🧪 Exemplo de Teste

```python
# src/shared_kernel/tests/test_aggregate_root.py
import pytest
from src.shared_kernel.domain.aggregate_root import AggregateRoot
from src.shared_kernel.domain.domain_event import DomainEvent


class UserCreatedEvent(DomainEvent):
    def __init__(self, user_id: str):
        super().__init__()
        self.user_id = user_id


class User(AggregateRoot):
    def __init__(self, user_id: str, name: str):
        super().__init__()
        self.id = user_id
        self.name = name
        self.add_domain_event(UserCreatedEvent(user_id))


def test_aggregate_root_collects_domain_events():
    user = User("123", "John Doe")
    
    events = user.domain_events
    
    assert len(events) == 1
    assert isinstance(events[0], UserCreatedEvent)
    assert events[0].user_id == "123"


def test_aggregate_root_clears_domain_events():
    user = User("123", "John Doe")
    
    user.clear_domain_events()
    
    assert len(user.domain_events) == 0
```

---

## ✅ Critérios de Aceitação

1. ✅ Todos os serviços Docker sobem sem erros
2. ✅ Testes de exemplo executam com sucesso
3. ✅ Pre-commit hooks funcionam
4. ✅ Cobertura de testes > 90% (nos arquivos de exemplo)
5. ✅ Complexidade ciclomática < 10
6. ✅ Documentação de setup completa
7. ✅ ADRs principais criados

---

## 🚀 Comandos Úteis

```bash
# Setup inicial
poetry install
pre-commit install

# Subir ambiente
docker-compose up -d

# Executar testes
pytest

# Cobertura
pytest --cov=src --cov-report=html

# Linting
black src/
isort src/
flake8 src/
mypy src/

# Mutation testing
mutmut run

# Logs
docker-compose logs -f backend
```

---

## 📚 Referências

- [Domain-Driven Design - Eric Evans](https://www.domainlanguage.com/ddd/)
- [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Cyclomatic Complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity)
- [C4 Model](https://c4model.com/)

---

**Próxima Sprint**: Sprint 1 - Admin Context (Autenticação e Governança)
