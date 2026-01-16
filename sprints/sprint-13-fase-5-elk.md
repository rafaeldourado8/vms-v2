# Sprint 13 Fase 5 - ELK Stack

## Implementação Completa

### 1. Componentes

#### Elasticsearch
- **Porta**: 9200
- **Função**: Armazenamento e indexação de logs
- **Índices**:
  - `gtvision-audit-*`: Logs de auditoria de segurança
  - `gtvision-application-*`: Logs de aplicação

#### Logstash
- **Porta**: 5000 (TCP)
- **Função**: Pipeline de processamento de logs
- **Filtros**:
  - Parse de timestamp
  - Separação de logs de auditoria e aplicação
  - Adição de tags e campos

#### Kibana
- **Porta**: 5601
- **Função**: Visualização e análise de logs
- **Dashboards**: Criar manualmente após iniciar

### 2. Arquitetura

```
Application → ELK Logger → Logstash → Elasticsearch → Kibana
                (TCP 5000)            (Index)        (Visualize)
```

### 3. Logs de Auditoria

#### Eventos Registrados
- **LOGIN**: Autenticação de usuário
- **LOGOUT**: Saída de usuário
- **DATA_ACCESS**: Acesso a dados pessoais (LGPD Art. 18 I/II)
- **DATA_EXPORT**: Exportação de dados (LGPD Art. 18 V)
- **DATA_DELETE**: Solicitação de exclusão (LGPD Art. 18 IV)
- **CONSENT_REVOKED**: Revogação de consentimento (LGPD Art. 18 IX)

#### Estrutura do Log
```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "audit_action": "LOGIN",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "ip_address": "192.168.1.100",
  "resource": "/api/auth/login",
  "details": {},
  "service": "streaming"
}
```

### 4. Quick Start

```bash
# Iniciar ELK Stack
scripts\start-elk.bat

# Verificar Elasticsearch
curl http://localhost:9200/_cluster/health

# Acessar Kibana
http://localhost:5601

# Executar testes E2E
venv\Scripts\pytest src/streaming/tests/e2e/test_elk_e2e.py -v
```

### 5. Kibana - Configuração Manual

#### Criar Index Pattern
1. Acessar Kibana: http://localhost:5601
2. Menu → Stack Management → Index Patterns
3. Criar pattern: `gtvision-audit-*`
4. Time field: `@timestamp`
5. Criar pattern: `gtvision-application-*`

#### Visualizar Logs
1. Menu → Discover
2. Selecionar index pattern
3. Filtrar por campos:
   - `audit_action`
   - `user_id`
   - `ip_address`
   - `resource`

### 6. Queries Úteis

#### Buscar logins de usuário específico
```json
GET /gtvision-audit-*/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"audit_action": "LOGIN"}},
        {"match": {"user_id": "123e4567-e89b-12d3-a456-426614174000"}}
      ]
    }
  }
}
```

#### Buscar ações LGPD
```json
GET /gtvision-audit-*/_search
{
  "query": {
    "terms": {
      "audit_action": ["DATA_ACCESS", "DATA_EXPORT", "DATA_DELETE", "CONSENT_REVOKED"]
    }
  }
}
```

#### Contar ações por tipo
```json
GET /gtvision-audit-*/_search
{
  "size": 0,
  "aggs": {
    "actions": {
      "terms": {"field": "audit_action.keyword"}
    }
  }
}
```

### 7. Compliance LGPD

#### Rastreabilidade
- Todos os acessos a dados pessoais são registrados
- Logs incluem: usuário, timestamp, IP, recurso acessado
- Retenção: 5 anos (conforme LGPD)

#### Auditoria
- Logs imutáveis no Elasticsearch
- Busca por período, usuário, ação
- Exportação para relatórios de compliance

### 8. Testes

```bash
# E2E ELK Stack
venv\Scripts\pytest src/streaming/tests/e2e/test_elk_e2e.py -v

# Todos os testes
venv\Scripts\pytest src/streaming/tests/ -v
```

### 9. Troubleshooting

#### Elasticsearch não inicia
```bash
# Verificar logs
docker logs gtvision-elasticsearch-dev

# Aumentar memória (docker-compose.dev.yml)
ES_JAVA_OPTS=-Xms1g -Xmx1g
```

#### Logs não aparecem no Kibana
```bash
# Verificar Logstash
docker logs gtvision-logstash-dev

# Testar conexão
telnet localhost 5000

# Verificar índices
curl http://localhost:9200/_cat/indices
```

### 10. Produção

#### Recomendações
- Cluster Elasticsearch (3+ nodes)
- Retenção de logs: 90 dias (hot) + 5 anos (cold)
- Backup diário dos índices
- Alertas para falhas de auditoria
- TLS/SSL para comunicação
- Autenticação X-Pack

## Status

✅ **COMPLETO**
- Elasticsearch configurado
- Logstash com pipeline de auditoria
- Kibana para visualização
- ELK Logger integrado
- Logs de segurança e LGPD
- Testes E2E
- Documentação
