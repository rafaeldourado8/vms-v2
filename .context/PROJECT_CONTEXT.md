# GT-Vision VMS - Contexto do Projeto

## 🎯 PROMPT PARA ASSISTENTES DE IA

**IMPORTANTE**: Leia este documento COMPLETAMENTE antes de fazer qualquer alteração no projeto.

---

## 📌 Contexto Atual do Projeto

Você está trabalhando no **GT-Vision VMS**, um sistema VMS (Video Management System) enterprise para prefeituras brasileiras.

### Status Atual: SPRINT 0 - Fundação e Arquitetura
- ✅ Planejamento completo de 20 sprints criado
- ✅ Estrutura de pastas inicial criada
- ⏳ Aguardando início da implementação da Sprint 0

---

## 🏗️ Arquitetura e Princípios (OBRIGATÓRIOS)

### Arquitetura
- **Estilo**: Monolito Modular
- **Padrão**: Domain-Driven Design (DDD)
- **Princípios**: SOLID
- **Complexidade Ciclomática**: Máximo 10 por função
- **Cobertura de Testes**: Mínimo 90%

### Bounded Contexts (DDD)
1. **Admin** - Governança total, autenticação, gestão de usuários admin
2. **Cidades** - Gestão de prefeituras, câmeras (até 1000 por prefeitura), planos de armazenamento
3. **Streaming** - Ingestão RTSP, HLS/WebRTC, gravação cíclica, timeline, clipping, mosaico
4. **AI** - Recepção de eventos LPR (License Plate Recognition), armazenamento, busca

### Estrutura DDD por Bounded Context
```
bounded_context/
├── domain/
│   ├── aggregates/      # Raízes de agregação
│   ├── entities/        # Entidades
│   ├── value_objects/   # Objetos de valor
│   ├── domain_events/   # Eventos de domínio
│   ├── repositories/    # Interfaces de repositórios
│   └── services/        # Serviços de domínio
├── application/
│   ├── use_cases/       # Casos de uso
│   ├── dtos/            # Data Transfer Objects
│   ├── event_handlers/  # Handlers de eventos
│   └── services/        # Serviços de aplicação
├── infrastructure/
│   ├── persistence/     # Implementação de repositórios
│   ├── messaging/       # RabbitMQ, eventos
│   ├── external_services/ # APIs externas
│   └── web/             # FastAPI/Django
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

---

## 🛠️ Stack Tecnológica

### Backend
- **Admin + Cidades**: Django 5.0 + Django REST Framework
- **Streaming + AI**: FastAPI (máxima performance)
- **Linguagem**: Python 3.11+

### Infraestrutura
- **Banco de Dados**: PostgreSQL 15
- **Cache**: Redis 7
- **Message Broker**: RabbitMQ 3
- **Streaming**: MediaMTX (RTSP/HLS/WebRTC)
- **Proxy/Gateway**: HAProxy + Kong
- **Processamento de Vídeo**: FFmpeg

### Observabilidade
- **Métricas**: Prometheus + Grafana
- **Logs**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Tracing**: (a definir)

### Deploy
- **Containerização**: Docker + Docker Compose
- **IaC**: Terraform (AWS)
- **CI/CD**: GitHub Actions
- **Cloud**: AWS (ECS/EKS, RDS, ElastiCache, S3, CloudFront)

---

## 📋 Requisitos Funcionais Principais

### 1. Admin Context
- Autenticação JWT com refresh tokens
- RBAC (Role-Based Access Control)
- Gestão de usuários admin
- Auditoria completa de ações
- Django Admin customizado

### 2. Cidades Context
- CRUD de prefeituras
- Planos de armazenamento: 7, 15 ou 30 dias (cíclico)
- Gestão de usuários por prefeitura:
  - 1 usuário gestor (CRUD completo)
  - 5 usuários visualizadores (somente leitura)
- CRUD de câmeras (até 1000 por prefeitura)
- Metadados: nome, localização, URL RTSP, status

### 3. Streaming Context
- **Ingestão RTSP**: Receber streams de câmeras IP
- **Streaming de Alta Qualidade**:
  - HLS adaptativo
  - WebRTC (latência ultra-baixa)
  - Zero latência percebida
- **Gravação Cíclica**:
  - Gravação contínua 24/7
  - Retenção conforme plano (7/15/30 dias)
  - Armazenamento em S3/MinIO
  - Limpeza automática de arquivos antigos
- **Timeline Interativa**:
  - Busca de gravações por período
  - Playback de gravações
  - Navegação rápida (seek)
  - Thumbnails para preview
  - Similar ao Camerite
- **Clipping**:
  - Criar clipes de vídeo (início + fim)
  - Processamento assíncrono (RabbitMQ)
  - Download de clipes
- **Mosaico**:
  - Visualização de múltiplas câmeras
  - Máximo 4 câmeras por mosaico (economia de recursos)
  - Layouts 2x2
  - Salvamento de configurações

### 4. AI Context
- **Eventos LPR** (License Plate Recognition):
  - Webhook para receber eventos das câmeras
  - Armazenamento de metadados (placa, timestamp, câmera, imagem)
  - Busca avançada (placa, período, câmera, cidade)
  - Exportação de relatórios (CSV, PDF)
  - Estatísticas

**IMPORTANTE**: Não vamos desenvolver IA de detecção. As câmeras já possuem IA embarcada e enviam eventos via webhook.

---

## 🔒 Requisitos Não-Funcionais

### Segurança
- **OWASP Top 10**: Todas as proteções implementadas
- **LGPD**: Compliance total
- Rate limiting (Kong)
- CORS configurado
- JWT com refresh tokens
- Sanitização de inputs
- SQL injection prevention
- XSS prevention
- CSRF tokens
- HTTPS obrigatório (produção)
- Secrets Manager (AWS)

### Performance
- Latência streaming: < 500ms
- API response time: < 200ms (p95)
- Uptime: > 99.9%
- Suporte a 1000 câmeras simultâneas
- 100 usuários simultâneos
- 10.000 eventos LPR/hora

### Qualidade de Código
- Cobertura de testes: > 90%
- Complexidade ciclomática: < 10 por função
- Maintainability Index: > 70
- Code Smells: 0 críticos
- Duplicação: < 3%

### Testes
- **Unitários**: pytest (>90% coverage)
- **Integração**: pytest-django, pytest-asyncio
- **E2E**: Cypress/Playwright
- **Carga**: Locust/K6
- **Mutação**: mutmut
- **Caos**: Chaos Monkey

---

## 📁 Estrutura de Pastas Atual

```
GT-Vision-VMS/
├── src/
│   ├── admin/           # Bounded Context: Admin
│   ├── cidades/         # Bounded Context: Cidades
│   ├── streaming/       # Bounded Context: Streaming
│   └── ai/              # Bounded Context: AI
├── haproxy/
│   └── haproxy.cfg      # ✅ Já configurado
├── kong/
│   └── kong.yml         # ✅ Já configurado
├── mediamtx.yml         # ✅ Já configurado
├── sprints/
│   ├── README.md        # ✅ Planejamento completo (20 sprints)
│   └── sprint-0.md      # ✅ Sprint 0 detalhada
└── .context/
    └── PROJECT_CONTEXT.md  # ✅ Este arquivo
```

---

## 📅 Planejamento de Sprints

### Timeline: 20 sprints (~7 meses)

1. **Sprint 0** (5 dias): Fundação e Arquitetura ⏳ ATUAL
2. **Sprint 1** (7 dias): Admin - Autenticação
3. **Sprint 2** (7 dias): Cidades - Gestão de Prefeituras
4. **Sprint 3** (7 dias): Cidades - Gestão de Câmeras
5. **Sprint 4** (10 dias): Streaming - Ingestão RTSP
6. **Sprint 5** (10 dias): Streaming - HLS/WebRTC
7. **Sprint 6** (10 dias): Streaming - Gravação Cíclica
8. **Sprint 7** (10 dias): Streaming - Timeline e Playback
9. **Sprint 8** (7 dias): Streaming - Clipping
10. **Sprint 9** (7 dias): Streaming - Mosaico
11. **Sprint 10** (7 dias): AI - Recepção de Eventos LPR
12. **Sprint 11** (5 dias): AI - Busca e Exibição
13. **Sprint 12** (5 dias): Observabilidade - Prometheus + Grafana
14. **Sprint 13** (5 dias): Logs e Segurança
15. **Sprint 14** (5 dias): LGPD - Compliance
16. **Sprint 15** (7 dias): Integração Frontend
17. **Sprint 16** (7 dias): Testes de Carga e Performance
18. **Sprint 17** (7 dias): Terraform - IaC AWS
19. **Sprint 18** (5 dias): CI/CD Pipeline
20. **Sprint 19** (5 dias): Documentação Final
21. **Sprint 20** (7 dias): Testes Finais e Homologação

**Detalhes completos**: Ver `sprints/README.md`

---

## 🚨 REGRAS CRÍTICAS (NUNCA VIOLAR)

### 1. DDD e SOLID
- ✅ SEMPRE seguir a estrutura DDD (domain/application/infrastructure)
- ✅ SEMPRE aplicar princípios SOLID
- ✅ Domain layer NUNCA depende de infrastructure
- ✅ Use cases SEMPRE no application layer
- ✅ Repositories são SEMPRE interfaces no domain

### 2. Complexidade e Qualidade
- ✅ Complexidade ciclomática < 10 por função
- ✅ Cobertura de testes > 90%
- ✅ SEMPRE escrever testes antes ou junto com o código
- ✅ SEMPRE usar type hints (Python)
- ✅ SEMPRE documentar funções públicas

### 3. Código Limpo
- ✅ Nomes descritivos (sem abreviações)
- ✅ Funções pequenas (máximo 20 linhas)
- ✅ Single Responsibility Principle
- ✅ Evitar comentários (código auto-explicativo)
- ✅ SEMPRE usar black, isort, flake8, mypy

### 4. Segurança
- ✅ NUNCA commitar credenciais
- ✅ SEMPRE usar variáveis de ambiente
- ✅ SEMPRE validar inputs
- ✅ SEMPRE sanitizar outputs
- ✅ SEMPRE usar prepared statements (SQL)

### 5. Performance
- ✅ SEMPRE usar índices em queries frequentes
- ✅ SEMPRE usar cache (Redis) quando apropriado
- ✅ SEMPRE usar async/await em I/O (FastAPI)
- ✅ SEMPRE usar connection pooling

### 6. Logs e Observabilidade
- ✅ SEMPRE logar ações importantes
- ✅ SEMPRE usar logs estruturados (JSON)
- ✅ SEMPRE incluir correlation_id
- ✅ SEMPRE expor métricas (Prometheus)

---

## 🎯 Próximos Passos Imediatos

### Sprint 0 - Tarefas Pendentes:

1. **Criar Shared Kernel** (src/shared_kernel/)
   - domain/aggregate_root.py
   - domain/entity.py
   - domain/value_object.py
   - domain/domain_event.py
   - domain/domain_exception.py
   - domain/repository.py
   - application/use_case.py
   - application/event_bus.py
   - infrastructure/database.py
   - infrastructure/cache.py
   - infrastructure/message_broker.py

2. **Criar Docker Compose completo**
   - PostgreSQL, Redis, RabbitMQ
   - Backend (Django), Streaming (FastAPI)
   - MediaMTX, HAProxy, Kong
   - Prometheus, Grafana
   - ELK Stack

3. **Configurar ferramentas de qualidade**
   - pyproject.toml
   - pytest.ini
   - .flake8
   - mypy.ini
   - .pre-commit-config.yaml

4. **Criar ADRs**
   - ADR 001: Arquitetura DDD + Monolito Modular
   - ADR 002: Escolha de tecnologias

5. **Documentação**
   - README.md principal
   - docs/development/setup.md

---

## 💬 Como Usar Este Contexto

### Para Assistentes de IA:

Quando você receber uma solicitação relacionada a este projeto:

1. **SEMPRE leia este arquivo primeiro**
2. **SEMPRE verifique a sprint atual** (sprints/README.md)
3. **SEMPRE siga a arquitetura DDD**
4. **SEMPRE respeite as regras críticas**
5. **SEMPRE escreva código mínimo e funcional**
6. **SEMPRE escreva testes**
7. **SEMPRE documente decisões importantes**

### Comandos Úteis:

```bash
# Ver contexto atual
cat .context/PROJECT_CONTEXT.md

# Ver sprint atual
cat sprints/sprint-0.md

# Ver planejamento completo
cat sprints/README.md
```

---

## 📝 Histórico de Decisões

### 2025-01-XX - Início do Projeto
- ✅ Arquitetura DDD + Monolito Modular definida
- ✅ Stack tecnológica escolhida
- ✅ 20 sprints planejadas
- ✅ MediaMTX, HAProxy, Kong pré-configurados
- ⏳ Aguardando início da Sprint 0

---

## 🔗 Links Importantes

- **Sprints**: `sprints/README.md`
- **Sprint Atual**: `sprints/sprint-0.md`
- **MediaMTX Config**: `mediamtx.yml`
- **HAProxy Config**: `haproxy/haproxy.cfg`
- **Kong Config**: `kong/kong.yml`

---

## 📞 Contato e Suporte

Para dúvidas sobre o projeto, sempre consulte:
1. Este arquivo (.context/PROJECT_CONTEXT.md)
2. Planejamento de sprints (sprints/README.md)
3. Sprint atual (sprints/sprint-X.md)

---

**Última atualização**: 2025-01-XX
**Versão**: 1.0
**Status**: Sprint 0 - Fundação e Arquitetura (em preparação)

---

## 🚀 PROMPT RÁPIDO PARA ASSISTENTES

```
Você está trabalhando no GT-Vision VMS, um sistema VMS enterprise para prefeituras.

ARQUITETURA: DDD + SOLID + Monolito Modular
SPRINT ATUAL: Sprint 0 - Fundação e Arquitetura
STACK: Django + FastAPI + PostgreSQL + Redis + RabbitMQ + MediaMTX

REGRAS OBRIGATÓRIAS:
- Complexidade ciclomática < 10
- Cobertura de testes > 90%
- Seguir estrutura DDD (domain/application/infrastructure)
- SOLID em todo código
- Type hints obrigatórios
- Código mínimo e funcional

LEIA: .context/PROJECT_CONTEXT.md para contexto completo
LEIA: sprints/sprint-0.md para tarefas atuais
```
