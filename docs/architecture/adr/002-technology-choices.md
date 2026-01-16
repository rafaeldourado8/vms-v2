# ADR 002: Escolha de Tecnologias

## Status
Aceito

## Contexto
Precisamos escolher tecnologias que atendam:
- Performance para streaming de vídeo
- Escalabilidade horizontal
- Maturidade e suporte da comunidade
- Facilidade de contratação de desenvolvedores
- Custo de infraestrutura

## Decisão

### Backend
- **Django 5.0 + DRF** (Admin + Cidades)
  - Maturidade e estabilidade
  - Django Admin pronto
  - ORM robusto
  - Ecossistema rico
  
- **FastAPI** (Streaming + AI)
  - Performance superior (async)
  - Type hints nativos
  - Documentação automática
  - Ideal para I/O intensivo

### Database
- **PostgreSQL 15**
  - ACID completo
  - JSON support
  - Extensões (PostGIS futuro)
  - Performance comprovada

### Cache
- **Redis 7**
  - Performance excepcional
  - Pub/Sub para eventos
  - Estruturas de dados ricas
  - Persistência opcional

### Message Broker
- **RabbitMQ 3**
  - Confiabilidade
  - Dead letter queues
  - Retry policies
  - Management UI

### Streaming
- **MediaMTX**
  - RTSP/HLS/WebRTC
  - Baixa latência
  - API REST
  - Open source

### Proxy/Gateway
- **HAProxy** - Load balancing
- **Kong** - API Gateway, rate limiting

### Observabilidade
- **Prometheus** - Métricas
- **Grafana** - Dashboards
- **ELK Stack** - Logs centralizados

### Deploy
- **Docker Compose** - Desenvolvimento
- **Terraform** - IaC para AWS
- **AWS ECS/EKS** - Produção

## Consequências

### Positivas
- Stack moderna e performática
- Boa documentação disponível
- Comunidade ativa
- Facilidade de contratação
- Custo-benefício adequado

### Negativas
- Múltiplas linguagens (Python)
- Curva de aprendizado (FastAPI, MediaMTX)
- Complexidade operacional (múltiplos serviços)

## Alternativas Consideradas

### Backend
1. **Node.js + Express**
   - ❌ Menos estruturado
   - ❌ Ecossistema fragmentado
   
2. **Go**
   - ✅ Performance superior
   - ❌ Menos desenvolvedores
   - ❌ Menos bibliotecas

### Database
1. **MySQL**
   - ❌ Menos features
   - ❌ JSON support inferior
   
2. **MongoDB**
   - ❌ Não é ACID
   - ❌ Não adequado para transações

### Streaming
1. **Wowza**
   - ❌ Custo alto
   - ❌ Closed source
   
2. **Nginx-RTMP**
   - ❌ Menos features
   - ❌ Sem WebRTC nativo

## Referências
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [MediaMTX GitHub](https://github.com/bluenviron/mediamtx)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
