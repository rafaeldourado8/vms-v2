# GT-Vision VMS - Testes

## Estrutura de Testes

```
tests/
├── unit/                    # Testes unitários (isolados)
├── integration/             # Testes de integração (componentes)
│   ├── test_haproxy.py     # HAProxy (5 testes)
│   ├── test_kong.py        # Kong Gateway (6 testes)
│   ├── test_auth.py        # Autenticação (4 testes)
│   └── test_lgpd.py        # LGPD (5 testes)
└── e2e/                     # Testes E2E (fluxo completo)
    └── test_full_flow.py   # Fluxo completo (8 testes)
```

## Executar Testes

### Todos os Testes
```bash
poetry run pytest tests/ -v
```

### Por Tipo
```bash
# Unitários
poetry run pytest tests/unit/ -v

# Integração
poetry run pytest tests/integration/ -v

# E2E
poetry run pytest tests/e2e/ -v -m e2e
```

### Por Sprint
```bash
# Sprint 13 (Segurança + HAProxy + Kong + E2E)
scripts\test-sprint13.bat

# Sprint 12 (Observabilidade)
poetry run pytest tests/ -k "prometheus or grafana" -v

# Sprint 11 (Integração)
poetry run pytest tests/ -k "postgresql or rabbitmq or minio" -v
```

### Com Cobertura
```bash
poetry run pytest tests/ --cov=src --cov-report=html
```

## Testes por Componente

### HAProxy (5 testes)
```bash
poetry run pytest tests/integration/test_haproxy.py -v
```

- Stats dashboard disponível
- Health check endpoint
- Roteamento para backends
- Rate limiting (429)
- Security headers

### Kong Gateway (6 testes)
```bash
poetry run pytest tests/integration/test_kong.py -v
```

- Kong health check
- Roteamento para serviços
- Rate limiting (429 após 10 req)
- CORS headers
- JWT obrigatório (401)

### E2E Full Flow (8 testes)
```bash
poetry run pytest tests/e2e/test_full_flow.py -v -m e2e
```

- Criar câmera → Iniciar stream
- Webhook LPR → Buscar detecções
- Segurança (401, 429, audit)
- Observabilidade (Prometheus, Grafana, ELK)
- RabbitMQ, MediaMTX, MinIO
- API response time (<200ms)

## Requisitos

### Serviços Necessários
- PostgreSQL (porta 5432)
- Redis (porta 6379)
- RabbitMQ (porta 5672, 15672)
- MinIO (porta 9000)
- MediaMTX (porta 8554, 8888, 8889)
- HAProxy (porta 80, 8404)
- Kong (porta 8000)
- Prometheus (porta 9090)
- Grafana (porta 3000)
- Elasticsearch (porta 9200)
- Kibana (porta 5601)

### Iniciar Serviços
```bash
# Infraestrutura completa
docker-compose -f docker-compose.dev.yml up -d

# Ou apenas o necessário
docker-compose up -d postgres redis rabbitmq minio mediamtx
```

## Markers

```python
@pytest.mark.unit          # Teste unitário
@pytest.mark.integration   # Teste de integração
@pytest.mark.e2e           # Teste E2E
@pytest.mark.slow          # Teste lento (>5s)
```

### Executar por Marker
```bash
pytest -m unit          # Apenas unitários
pytest -m integration   # Apenas integração
pytest -m e2e           # Apenas E2E
pytest -m "not slow"    # Excluir lentos
```

## Fixtures

### auth_token
```python
@pytest.fixture
def auth_token():
    """Retorna JWT token válido"""
    response = requests.post(
        "http://localhost:8001/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    return response.json()["access_token"]
```

### Uso
```python
def test_protected_endpoint(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get("/api/admin/users", headers=headers)
    assert response.status_code == 200
```

## Troubleshooting

### Testes Falhando

**Erro: Connection refused**
```bash
# Verificar se serviços estão rodando
docker-compose ps

# Iniciar serviços
docker-compose up -d
```

**Erro: 401 Unauthorized**
```bash
# Verificar se JWT está configurado
# Verificar se token está válido
```

**Erro: 429 Too Many Requests**
```bash
# Aguardar rate limit resetar (10s)
# Ou aumentar limite no Kong/HAProxy
```

## Cobertura

### Meta
- Unitários: >90%
- Integração: >80%
- E2E: Fluxos críticos

### Gerar Relatório
```bash
poetry run pytest --cov=src --cov-report=html
# Abrir: htmlcov/index.html
```

## CI/CD

### GitHub Actions
```yaml
- name: Run Tests
  run: |
    poetry install
    poetry run pytest tests/ -v --cov=src
```

### Pre-commit
```bash
# Instalar hooks
pre-commit install

# Executar manualmente
pre-commit run --all-files
```

## Estatísticas

**Total de Testes**: 48
- Unitários: 13
- Integração: 27
- E2E: 8

**Cobertura**: >90%

**Tempo de Execução**: ~2 minutos
