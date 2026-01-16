# Sprint 13 - Fase 4: ELK Stack ✅ COMPLETA

**Data**: 2025-01-16  
**Status**: ✅ COMPLETA  
**Tempo**: ~30 minutos

---

## 🎯 Objetivo

Implementar stack ELK (Elasticsearch + Logstash + Kibana) para centralizar logs de todos os serviços.

---

## ✅ Implementado

### 1. Logging Estruturado

#### JSONFormatter
- ✅ Formata logs como JSON
- ✅ Campos padrão: timestamp, level, logger, message, module, function, line
- ✅ Campos extras: user_id, correlation_id, audit_action, resource_type, resource_id
- ✅ Suporte a exceptions

**Arquivo**: `src/shared_kernel/infrastructure/logging_config.py`

#### LoggingMiddleware (FastAPI)
- ✅ Gera correlation_id para cada request
- ✅ Loga início e fim de requests
- ✅ Loga duração (ms)
- ✅ Loga erros com stack trace
- ✅ Adiciona X-Correlation-ID no response header

**Arquivo**: `src/streaming/infrastructure/web/middleware/logging_middleware.py`

### 2. Integração FastAPI

- ✅ setup_logging() chamado no startup
- ✅ LoggingMiddleware adicionado
- ✅ Logs enviados para Logstash (porta 5000)
- ✅ Fallback para console se Logstash indisponível

**Arquivo**: `src/streaming/infrastructure/web/main.py`

### 3. Logstash Pipeline

- ✅ Input: TCP porta 5000 (JSON)
- ✅ Filter: Parse timestamp, audit logs, application logs
- ✅ Output: Elasticsearch (índices por tipo e data)
- ✅ Output: stdout (debug)

**Arquivo**: `monitoring/logstash.conf`

### 4. Docker Compose

- ✅ Elasticsearch 8.11.0 (porta 9200)
- ✅ Logstash 8.11.0 (porta 5000)
- ✅ Kibana 8.11.0 (porta 5601)
- ✅ Volumes persistentes
- ✅ Health checks

**Arquivo**: `docker-compose.dev.yml`

### 5. Testes

#### Testes Unitários (3)
- ✅ test_format_basic_log
- ✅ test_format_with_extra_fields
- ✅ test_format_with_exception

#### Testes de Integração (2)
- ✅ test_setup_logging
- ✅ test_get_logger

#### Smoke Tests (5)
- ✅ test_elasticsearch_health
- ✅ test_logstash_health
- ✅ test_kibana_health
- ✅ test_logs_indexed_in_elasticsearch
- ✅ test_log_search_in_elasticsearch

**Arquivos**:
- `src/shared_kernel/tests/integration/test_logging.py`
- `src/shared_kernel/tests/integration/test_elk_stack.py`

---

## 📊 Estatísticas

- **Arquivos criados**: 6
- **Arquivos atualizados**: 1
- **Linhas escritas**: ~450 (Python)
- **Testes**: 10 (3 unit + 2 integration + 5 smoke)
- **Tempo**: ~30 minutos

---

## 🚀 Como Usar

### 1. Iniciar ELK Stack

```bash
# Iniciar todos os serviços
docker-compose -f docker-compose.dev.yml up -d

# Aguardar serviços iniciarem (30s)
timeout /t 30

# Verificar status
docker-compose -f docker-compose.dev.yml ps
```

### 2. Acessar Serviços

- **Elasticsearch**: http://localhost:9200
- **Kibana**: http://localhost:5601
- **Logstash**: localhost:5000 (TCP)

### 3. Verificar Logs no Elasticsearch

```bash
# Listar índices
curl http://localhost:9200/_cat/indices/gtvision-*

# Buscar logs
curl -X POST http://localhost:9200/gtvision-*/_search -H "Content-Type: application/json" -d "{\"query\":{\"match_all\":{}},\"size\":10}"
```

### 4. Visualizar no Kibana

1. Acesse http://localhost:5601
2. Menu → Stack Management → Index Patterns
3. Criar pattern: `gtvision-*`
4. Menu → Discover
5. Visualizar logs em tempo real

### 5. Executar Testes

```bash
# Testes unitários
poetry run pytest src/shared_kernel/tests/integration/test_logging.py -v

# Smoke tests (requer ELK rodando)
poetry run pytest src/shared_kernel/tests/integration/test_elk_stack.py -v
```

---

## 📋 Índices Elasticsearch

### gtvision-application-YYYY.MM.DD
Logs de aplicação (Django + FastAPI)

**Campos**:
- `@timestamp`: Timestamp do log
- `level`: INFO, WARNING, ERROR, CRITICAL
- `logger`: Nome do logger
- `message`: Mensagem do log
- `module`: Módulo Python
- `function`: Função Python
- `line`: Linha do código
- `correlation_id`: ID de correlação (requests)
- `user_id`: ID do usuário (se autenticado)

### gtvision-audit-YYYY.MM.DD
Logs de auditoria (LGPD)

**Campos**:
- `@timestamp`: Timestamp da ação
- `audit_action`: Ação executada (CREATE, UPDATE, DELETE, etc)
- `user_id`: ID do usuário
- `resource_type`: Tipo do recurso (camera, stream, etc)
- `resource_id`: ID do recurso
- `correlation_id`: ID de correlação

---

## 🎨 Dashboards Kibana (Sugeridos)

### 1. Application Logs
- Logs por nível (INFO, ERROR)
- Logs por módulo
- Top 10 erros
- Timeline de logs

### 2. Audit Trail
- Ações por usuário
- Ações por recurso
- Timeline de auditoria
- Alertas de ações suspeitas

### 3. Performance
- Duração de requests (p50, p95, p99)
- Requests por endpoint
- Erros por endpoint
- Correlation ID tracking

---

## 🔍 Queries Úteis

### Buscar logs de erro
```json
{
  "query": {
    "match": {
      "level": "ERROR"
    }
  }
}
```

### Buscar por correlation_id
```json
{
  "query": {
    "term": {
      "correlation_id": "abc-123"
    }
  }
}
```

### Buscar ações de auditoria
```json
{
  "query": {
    "bool": {
      "must": [
        {"exists": {"field": "audit_action"}},
        {"term": {"user_id": "user123"}}
      ]
    }
  }
}
```

---

## ✅ Critérios de Sucesso

- [x] Elasticsearch rodando e acessível
- [x] Logstash recebendo logs na porta 5000
- [x] Kibana acessível e conectado ao Elasticsearch
- [x] Logs estruturados em JSON
- [x] Correlation ID em todos os requests
- [x] Índices criados automaticamente
- [x] Logs pesquisáveis no Elasticsearch
- [x] 10 testes passing (100%)

---

## 🎯 Próximos Passos

1. ✅ **Fase 4 COMPLETA**
2. 🚀 **Próximo**: Fase 5 - HAProxy + Kong (validação)
3. 🚀 **Depois**: Fase 6 - Testes E2E completos

---

## 📝 Notas

- Elasticsearch usa 256MB RAM (configurável via ES_JAVA_OPTS)
- Logstash usa 128MB RAM (configurável via LS_JAVA_OPTS)
- Retenção de logs: 30 dias (configurar ILM policy)
- Logs são enviados via TCP (mais confiável que UDP)
- Fallback para console se Logstash indisponível

---

**Status**: ✅ FASE 4 COMPLETA  
**Progresso Sprint 13**: 60% (4/6 fases)  
**Próxima fase**: Fase 5 - HAProxy + Kong
