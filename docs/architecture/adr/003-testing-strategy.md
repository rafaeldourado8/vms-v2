# ADR 003: Estratégia de Testes

## Status
Aceito

## Contexto
Precisamos garantir qualidade de código com:
- Cobertura > 90%
- Testes rápidos e confiáveis
- Detecção precoce de bugs
- Confiança para refatoração

## Decisão

### Pirâmide de Testes

#### 1. Testes Unitários (70%)
- **Framework**: pytest
- **Escopo**: Domain + Application layers
- **Características**:
  - Rápidos (< 1s cada)
  - Isolados (sem I/O)
  - Cobertura > 95%
  - Mocks para dependências

#### 2. Testes de Integração (20%)
- **Framework**: pytest + pytest-django/pytest-asyncio
- **Escopo**: Infrastructure layer
- **Características**:
  - Database real (PostgreSQL test)
  - Redis test instance
  - RabbitMQ test instance
  - Rollback automático

#### 3. Testes E2E (10%)
- **Framework**: Playwright/Cypress
- **Escopo**: Fluxos críticos
- **Características**:
  - Ambiente completo
  - Dados de teste
  - Executados em CI/CD

### Testes Adicionais

#### Mutation Testing
- **Framework**: mutmut
- **Objetivo**: Validar qualidade dos testes
- **Frequência**: Semanal

#### Testes de Carga
- **Framework**: Locust
- **Cenários**:
  - 1000 câmeras simultâneas
  - 100 usuários simultâneos
  - 10.000 eventos LPR/hora

#### Testes de Caos
- **Framework**: Chaos Monkey
- **Cenários**:
  - Falha de serviços
  - Latência de rede
  - Perda de conexão

### Métricas de Qualidade

```python
# pytest.ini
[pytest]
addopts = 
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=90
```

### Estrutura de Testes

```
bounded_context/
└── tests/
    ├── unit/           # Testes unitários
    ├── integration/    # Testes de integração
    └── e2e/           # Testes end-to-end
```

## Consequências

### Positivas
- Alta confiança no código
- Refatoração segura
- Documentação viva
- Detecção precoce de bugs
- Menos bugs em produção

### Negativas
- Tempo inicial maior
- Manutenção de testes
- CI/CD mais lento
- Curva de aprendizado

## Alternativas Consideradas

### 1. Apenas Testes E2E
- ❌ Lentos
- ❌ Frágeis
- ❌ Difícil debugar

### 2. TDD Estrito
- ✅ Qualidade alta
- ❌ Produtividade inicial baixa
- ❌ Requer disciplina extrema

### 3. Sem Testes
- ❌ Inaceitável para sistema crítico
- ❌ Manutenção impossível

## Implementação

### Comando de Testes
```bash
# Unitários
pytest -m unit

# Integração
pytest -m integration

# E2E
pytest -m e2e

# Todos com cobertura
pytest --cov=src --cov-report=html
```

### CI/CD Pipeline
```yaml
- run: pytest -m unit
- run: pytest -m integration
- run: pytest --cov=src --cov-fail-under=90
```

## Referências
- [Test Pyramid - Martin Fowler](https://martinfowler.com/articles/practical-test-pyramid.html)
- [pytest Documentation](https://docs.pytest.org/)
- [Mutation Testing](https://en.wikipedia.org/wiki/Mutation_testing)
