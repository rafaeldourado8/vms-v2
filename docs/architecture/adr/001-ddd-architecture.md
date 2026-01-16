# ADR 001: Arquitetura DDD + Monolito Modular

## Status
Aceito | Atualizado: Sprint 11 (Jan 2025)

## Contexto
Precisamos definir a arquitetura do GT-Vision VMS que suporte:
- Escalabilidade para 1000 câmeras por prefeitura
- Manutenibilidade de longo prazo
- Separação clara de responsabilidades
- Facilidade de testes
- Possibilidade de evolução para microserviços no futuro

## Decisão
Adotamos **Domain-Driven Design (DDD)** com estilo **Monolito Modular**.

### Bounded Contexts:
1. **Admin** (Django) - Autenticação, governança, usuários admin
2. **Cidades** (Django) - Prefeituras, câmeras, planos
3. **Streaming** (FastAPI) - Ingestão RTSP, HLS/WebRTC, gravação
4. **AI** (FastAPI) - Eventos LPR, busca, análise

### Stack Tecnológica:
- **Backend Admin/Cidades**: Django 5.0 + DRF (porta 8000)
- **Backend Streaming/AI**: FastAPI (porta 8001)
- **Database**: PostgreSQL 15 (porta 5432)
- **Cache**: Redis 7 (porta 6379)
- **Message Broker**: RabbitMQ 3 (porta 5672)
- **Storage**: MinIO S3-compatible (porta 9000)
- **Streaming Server**: MediaMTX (RTSP 8554, HLS 8888)
- **Observability**: Prometheus + Grafana + ELK
- **Proxy**: HAProxy + Kong Gateway

### Estrutura por Context:
```
bounded_context/
├── domain/          # Lógica de negócio pura
├── application/     # Casos de uso
├── infrastructure/  # Implementações técnicas
└── tests/          # Testes isolados
```

### Princípios:
- **SOLID** em todo código
- **Complexidade ciclomática < 10**
- **Cobertura de testes > 90%**
- Domain layer independente de frameworks
- Comunicação entre contexts via eventos (RabbitMQ)
- Shared Kernel para código compartilhado
- Anti-Corruption Layer entre contexts

### Comunicação:
- **Síncrona**: REST API via Kong Gateway
- **Assíncrona**: RabbitMQ para eventos de domínio
- **Cache**: Redis para dados frequentes
- **Storage**: MinIO para vídeos e imagens

## Consequências

### Positivas
- Código organizado e manutenível
- Fácil de testar (domain isolado)
- Baixo acoplamento entre contexts
- Evolução gradual para microserviços possível
- Onboarding de novos devs facilitado
- Regras de negócio explícitas no domain

### Negativas
- Curva de aprendizado inicial (DDD)
- Mais código boilerplate
- Requer disciplina da equipe
- Overhead inicial de setup

## Alternativas Consideradas

### 1. MVC Tradicional (Django)
- ❌ Alto acoplamento
- ❌ Difícil de testar
- ❌ Lógica de negócio espalhada

### 2. Microserviços desde o início
- ❌ Complexidade operacional alta
- ❌ Overhead de comunicação
- ❌ Difícil de debugar
- ❌ Over-engineering para MVP

### 3. Clean Architecture
- ✅ Similar ao DDD
- ❌ Menos foco em domínio
- ❌ Menos padrões estabelecidos

## Referências
- [Domain-Driven Design - Eric Evans](https://www.domainlanguage.com/ddd/)
- [Implementing Domain-Driven Design - Vaughn Vernon](https://vaughnvernon.com/)
- [Modular Monolith - Kamil Grzybek](https://www.kamilgrzybek.com/design/modular-monolith-primer/)
