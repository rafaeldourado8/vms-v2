# Arquitetura GT-Vision VMS

## 📐 Visão Geral

Sistema VMS (Video Management System) baseado em **Domain-Driven Design (DDD)** com estilo **Monolito Modular**.

## 🏗️ Bounded Contexts

### 1. Admin Context
**Responsabilidade**: Governança total do sistema

- Autenticação e autorização
- Gestão de usuários admin
- RBAC (Role-Based Access Control)
- Auditoria de ações
- Logs de segurança

**Tecnologia**: Django 5.0 + DRF

### 2. Cidades Context
**Responsabilidade**: Gestão de prefeituras e câmeras

- CRUD de prefeituras
- Planos de armazenamento (7/15/30 dias)
- Gestão de usuários por prefeitura
- CRUD de câmeras (até 1000 por prefeitura)
- Validações de negócio

**Tecnologia**: Django 5.0 + DRF

### 3. Streaming Context
**Responsabilidade**: Streaming e gravação de vídeo

- Ingestão RTSP
- Streaming HLS/WebRTC
- Gravação cíclica
- Timeline e playback
- Clipping de vídeo
- Mosaico de câmeras

**Tecnologia**: FastAPI + MediaMTX + FFmpeg

### 4. AI Context
**Responsabilidade**: Eventos de IA (LPR)

- Recepção de eventos LPR
- Armazenamento de metadados
- Busca avançada
- Exportação de relatórios
- Estatísticas

**Tecnologia**: FastAPI

## 📊 Estrutura DDD

```
bounded_context/
├── domain/
│   ├── aggregates/      # Raízes de agregação
│   ├── entities/        # Entidades
│   ├── value_objects/   # Objetos de valor
│   ├── events/          # Eventos de domínio
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
    ├── unit/            # Testes unitários
    ├── integration/     # Testes de integração
    └── e2e/            # Testes end-to-end
```

## 🔄 Comunicação Entre Contexts

### Síncrona
- REST API (via Kong Gateway)
- Validações imediatas

### Assíncrona
- RabbitMQ (eventos de domínio)
- Processamento em background
- Eventual consistency

## 🎯 Princípios Arquiteturais

### 1. Dependency Rule
- Domain não depende de nada
- Application depende de Domain
- Infrastructure depende de Application e Domain

### 2. SOLID
- **S**ingle Responsibility
- **O**pen/Closed
- **L**iskov Substitution
- **I**nterface Segregation
- **D**ependency Inversion

### 3. Complexidade
- Máximo 10 por função (ciclomática)
- Funções pequenas (< 20 linhas)
- Classes coesas

### 4. Testes
- Cobertura > 90%
- Testes rápidos
- Isolamento completo

## 🔐 Segurança

### Camadas de Segurança
1. **HAProxy** - Rate limiting, SSL termination
2. **Kong** - API Gateway, autenticação, rate limiting
3. **Backend** - JWT, RBAC, validações
4. **Database** - Prepared statements, encryption at rest

### OWASP Top 10
- ✅ Broken Access Control
- ✅ Cryptographic Failures
- ✅ Injection
- ✅ Insecure Design
- ✅ Security Misconfiguration
- ✅ Vulnerable Components
- ✅ Authentication Failures
- ✅ Software Integrity Failures
- ✅ Logging Failures
- ✅ SSRF

## 📈 Escalabilidade

### Horizontal
- Stateless services
- Load balancing (HAProxy)
- Cache distribuído (Redis)
- Message broker (RabbitMQ)

### Vertical
- Connection pooling
- Query optimization
- Índices adequados
- Cache strategies

## 🔍 Observabilidade

### Métricas (Prometheus)
- Requests/segundo
- Latência (p50, p95, p99)
- Taxa de erros
- Uso de recursos

### Logs (ELK)
- Logs estruturados (JSON)
- Correlation ID
- Níveis adequados
- Retenção configurável

### Tracing
- Request tracing
- Performance profiling
- Bottleneck identification

## 📚 ADRs (Architecture Decision Records)

- [ADR 001: Arquitetura DDD + Monolito Modular](adr/001-ddd-architecture.md)
- [ADR 002: Escolha de Tecnologias](adr/002-technology-choices.md)
- [ADR 003: Estratégia de Testes](adr/003-testing-strategy.md)

## 🚀 Evolução Futura

### Fase 1: Monolito Modular (Atual)
- Desenvolvimento rápido
- Deploy simples
- Baixa complexidade operacional

### Fase 2: Microserviços (Futuro)
- Quando necessário (> 10 devs, > 10k câmeras)
- Migração gradual por context
- Mantém contratos de API

## 📖 Referências

- [Domain-Driven Design - Eric Evans](https://www.domainlanguage.com/ddd/)
- [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Modular Monolith - Kamil Grzybek](https://www.kamilgrzybek.com/design/modular-monolith-primer/)
