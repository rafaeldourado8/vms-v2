# GT-Vision VMS - Planejamento de Sprints

## 🎯 Visão Geral do Projeto

Sistema VMS (Video Management System) enterprise para prefeituras com arquitetura DDD, SOLID, monolito modular.

### Stack Tecnológica
- **Backend Admin**: Django + DRF (DDD, SOLID)
- **Backend Streaming**: FastAPI (máxima performance)
- **Frontend**: React (já desenvolvido - integração final)
- **Streaming**: MediaMTX (RTSP/HLS/WebRTC)
- **Message Broker**: RabbitMQ
- **Cache**: Redis
- **Proxy/Gateway**: HAProxy + Kong
- **Observabilidade**: Prometheus + Grafana
- **Logs**: ELK Stack
- **IaC**: Terraform (AWS)
- **CI/CD**: GitHub Actions
- **Containerização**: Docker + Docker Compose

### Bounded Contexts (DDD)
1. **Admin** - Governança total, autenticação, gestão de usuários
2. **Cidades** - Gestão de prefeituras, câmeras, planos
3. **Streaming** - Ingestão RTSP, HLS/WebRTC, gravação cíclica
4. **AI** - Recepção eventos LPR, armazenamento, exibição

---

## 📋 Sprints Detalhadas

### **SPRINT 0: Fundação e Arquitetura** (5 dias)
**Objetivo**: Estabelecer base sólida DDD, estrutura de pastas, configurações iniciais

#### Entregáveis:
- [ ] Estrutura DDD completa para todos os bounded contexts
- [ ] Shared Kernel (Value Objects, Domain Events, Exceptions)
- [ ] Docker Compose completo (dev environment)
- [ ] Configuração inicial PostgreSQL + Redis + RabbitMQ
- [ ] Setup de testes (pytest, coverage, mutation testing)
- [ ] Pre-commit hooks (black, flake8, mypy, isort)
- [ ] Documentação de arquitetura (ADRs)

#### Arquivos:
```
src/
├── shared_kernel/
│   ├── domain/
│   │   ├── value_objects.py
│   │   ├── domain_events.py
│   │   ├── aggregate_root.py
│   │   └── exceptions.py
│   ├── application/
│   │   ├── use_case.py
│   │   └── event_bus.py
│   └── infrastructure/
│       ├── database.py
│       ├── cache.py
│       └── message_broker.py
├── admin/
├── cidades/
├── streaming/
└── ai/
```

---

### **SPRINT 1: Admin Context - Autenticação e Governança** (7 dias)
**Objetivo**: Sistema de autenticação robusto, gestão de usuários admin

#### Entregáveis:
- [ ] Domain Layer: User, Role, Permission aggregates
- [ ] Application Layer: Use cases (CreateUser, Authenticate, ManagePermissions)
- [ ] Infrastructure: Django Admin customizado, JWT auth
- [ ] API REST: Endpoints de autenticação
- [ ] Testes unitários (>90% coverage)
- [ ] Testes de integração
- [ ] Documentação OpenAPI

#### Funcionalidades:
- Login/Logout com JWT
- Gestão de usuários admin
- RBAC (Role-Based Access Control)
- Auditoria de ações (Event Sourcing)
- Logs de segurança

#### Complexidade Ciclomática: < 10 por função

---

### **SPRINT 2: Cidades Context - Gestão de Prefeituras** (7 dias)
**Objetivo**: CRUD completo de prefeituras, planos de armazenamento

#### Entregáveis:
- [ ] Domain Layer: Cidade, Plano, Usuario aggregates
- [ ] Application Layer: Use cases (CreateCidade, AssignPlano, ManageUsers)
- [ ] Infrastructure: Repositories, Django Admin
- [ ] API REST: Endpoints de cidades
- [ ] Validações de negócio (max 1000 câmeras, 1 gestor + 5 visualizadores)
- [ ] Testes unitários + integração
- [ ] Documentação

#### Funcionalidades:
- CRUD Prefeituras
- Planos: 7/15/30 dias cíclicos
- Gestão de usuários por prefeitura (1 gestor + 5 visualizadores)
- Limites de câmeras (até 1000)

---

### **SPRINT 3: Cidades Context - Gestão de Câmeras** (7 dias)
**Objetivo**: CRUD de câmeras, associação com prefeituras

#### Entregáveis:
- [ ] Domain Layer: Camera aggregate
- [ ] Application Layer: Use cases (CreateCamera, UpdateCamera, DeleteCamera)
- [ ] Infrastructure: Repositories
- [ ] API REST: Endpoints de câmeras
- [ ] Integração com MediaMTX (provisionamento dinâmico)
- [ ] Validações (limite por prefeitura)
- [ ] Testes
- [ ] Documentação

#### Funcionalidades:
- CRUD Câmeras
- Metadados: nome, localização, URL RTSP, status
- Associação com prefeitura
- Validação de limites

---

### **SPRINT 4: Streaming Context - Ingestão RTSP** (10 dias)
**Objetivo**: Ingestão de streams RTSP, integração com MediaMTX

#### Entregáveis:
- [ ] FastAPI service (máxima performance)
- [ ] Domain Layer: Stream, Recording aggregates
- [ ] Application Layer: Use cases (StartStream, StopStream, HealthCheck)
- [ ] Infrastructure: MediaMTX API client, FFmpeg wrapper
- [ ] Provisionamento dinâmico de câmeras no MediaMTX
- [ ] Health checks de streams
- [ ] Testes de carga (locust)
- [ ] Documentação

#### Funcionalidades:
- Ingestão RTSP → MediaMTX
- Provisionamento automático via API
- Monitoramento de saúde dos streams
- Reconexão automática

---

### **SPRINT 5: Streaming Context - HLS/WebRTC Zero Latência** (10 dias)
**Objetivo**: Streaming de alta qualidade, zero latência

#### Entregáveis:
- [ ] Configuração otimizada MediaMTX (HLS + WebRTC)
- [ ] API endpoints para obter URLs de streaming
- [ ] WebSocket para eventos de streaming
- [ ] Otimizações de performance (buffer, segmentos)
- [ ] Testes de latência
- [ ] Documentação

#### Funcionalidades:
- HLS adaptativo (qualidade automática)
- WebRTC para latência ultra-baixa
- Fallback automático HLS ↔ WebRTC
- Métricas de qualidade (bitrate, fps, latência)

---

### **SPRINT 6: Streaming Context - Gravação Cíclica** (10 dias)
**Objetivo**: Sistema de gravação contínua com retenção por plano

#### Entregáveis:
- [ ] Domain Layer: Recording, RetentionPolicy aggregates
- [ ] Application Layer: Use cases (StartRecording, ManageRetention)
- [ ] Infrastructure: FFmpeg recording, S3/MinIO storage
- [ ] Worker assíncrono (RabbitMQ) para gravação
- [ ] Limpeza automática (cron jobs)
- [ ] Testes
- [ ] Documentação

#### Funcionalidades:
- Gravação contínua RTSP → MP4/FMP4
- Retenção: 7/15/30 dias (por plano)
- Armazenamento: S3/MinIO
- Limpeza automática de arquivos antigos
- Indexação para busca rápida

---

### **SPRINT 7: Streaming Context - Timeline e Playback** (10 dias) ✅ COMPLETA
**Objetivo**: Timeline interativa, playback de gravações

**Status**: ✅ COMPLETA (2025-01-16)

#### Entregáveis:
- [x] API de busca de gravações por período
- [x] Geração de thumbnails (FFmpeg)
- [x] Endpoint de playback (HLS de arquivos gravados)
- [x] Timeline metadata (eventos, gaps)
- [x] Testes
- [x] Documentação

#### Funcionalidades:
- Busca de gravações por câmera + período
- Timeline visual (similar Camerite)
- Playback de gravações via HLS
- Thumbnails para preview
- Navegação rápida (seek)

#### Documentação:
- [Sprint 7 - Documentação Completa](sprint-7.md)
- [Sprint 7 - Checklist](sprint-7-checklist.md)
- [Sprint 7 - Resumo Executivo](sprint-7-summary.md)
- [Sprint 7 - Índice](sprint-7-index.md)

---

### **SPRINT 8: Streaming Context - Clipping de Vídeo** (7 dias)
**Objetivo**: Recorte e exportação de clipes

#### Entregáveis:
- [ ] Domain Layer: Clip aggregate
- [ ] Application Layer: Use case (CreateClip)
- [ ] Infrastructure: FFmpeg clipping, async processing
- [ ] API endpoints (criar, listar, download)
- [ ] Worker RabbitMQ para processamento
- [ ] Testes
- [ ] Documentação

#### Funcionalidades:
- Criar clipe (câmera + início + fim)
- Processamento assíncrono (RabbitMQ)
- Download de clipes
- Gestão de clipes (listar, deletar)

---

### **SPRINT 9: Streaming Context - Mosaico** (7 dias)
**Objetivo**: Visualização de múltiplas câmeras (4 por mosaico)

#### Entregáveis:
- [ ] Domain Layer: Mosaic aggregate
- [ ] Application Layer: Use cases (CreateMosaic, UpdateMosaic)
- [ ] API endpoints (CRUD mosaicos)
- [ ] Otimização de recursos (max 4 câmeras)
- [ ] Testes
- [ ] Documentação

#### Funcionalidades:
- CRUD Mosaicos
- Associação de até 4 câmeras por mosaico
- Layouts predefinidos (2x2)
- Salvamento de configurações

---

### **SPRINT 10: AI Context - Recepção de Eventos LPR** (7 dias)
**Objetivo**: Receber e armazenar eventos de LPR das câmeras

#### Entregáveis:
- [ ] Domain Layer: LPREvent aggregate
- [ ] Application Layer: Use case (ReceiveLPREvent)
- [ ] Infrastructure: Webhook receiver, Repository
- [ ] API endpoints (receber eventos, listar)
- [ ] Armazenamento de imagens (S3/MinIO)
- [ ] Testes
- [ ] Documentação

#### Funcionalidades:
- Webhook para receber eventos LPR
- Armazenamento de metadados (placa, timestamp, câmera, imagem)
- Busca de eventos por placa/período/câmera
- Armazenamento de imagens de evidência

---

### **SPRINT 11: AI Context - Busca e Exibição de Eventos** (5 dias)
**Objetivo**: API de busca avançada de eventos LPR

#### Entregáveis:
- [ ] API de busca (filtros: placa, período, câmera, cidade)
- [ ] Paginação e ordenação
- [ ] Exportação de relatórios (CSV, PDF)
- [ ] Testes
- [ ] Documentação

#### Funcionalidades:
- Busca avançada de eventos LPR
- Filtros múltiplos
- Exportação de dados
- Estatísticas (eventos por período)

---

### **SPRINT 12: Observabilidade - Prometheus + Grafana** (5 dias)
**Objetivo**: Monitoramento completo do sistema

#### Entregáveis:
- [ ] Prometheus configurado (scraping de métricas)
- [ ] Grafana dashboards:
  - Visão geral do sistema
  - Streaming (latência, bitrate, fps)
  - Câmeras (status, uptime)
  - Recursos (CPU, RAM, disco)
  - Eventos LPR
- [ ] Alertas (Alertmanager)
- [ ] Documentação

#### Métricas:
- Streams ativos
- Latência média
- Taxa de erros
- Uso de recursos
- Eventos LPR/hora

---

### **SPRINT 13: Logs e Segurança** (5 dias)
**Objetivo**: Sistema de logs centralizado, segurança OWASP

#### Entregáveis:
- [ ] ELK Stack (Elasticsearch, Logstash, Kibana)
- [ ] Logs estruturados (JSON)
- [ ] Logs de auditoria (todas as ações)
- [ ] Logs de segurança (tentativas de acesso)
- [ ] Análise OWASP Top 10
- [ ] Implementação de proteções (rate limiting, CORS, CSP)
- [ ] Documentação

#### Segurança:
- Rate limiting (Kong)
- CORS configurado
- JWT com refresh tokens
- Sanitização de inputs
- SQL injection prevention
- XSS prevention
- CSRF tokens
- HTTPS obrigatório (produção)

---

### **SPRINT 14: LGPD - Compliance** (5 dias)
**Objetivo**: Adequação à LGPD

#### Entregáveis:
- [ ] Política de privacidade
- [ ] Termo de consentimento
- [ ] Anonimização de dados sensíveis
- [ ] Direito ao esquecimento (delete cascade)
- [ ] Logs de acesso a dados pessoais
- [ ] Documentação de tratamento de dados
- [ ] Relatório de impacto (RIPD)

---

### **SPRINT 15: Integração Frontend** (7 dias)
**Objetivo**: Conectar frontend aos endpoints backend

#### Entregáveis:
- [ ] Integração de todos os endpoints
- [ ] Testes E2E (Cypress/Playwright)
- [ ] Ajustes de UX/UI
- [ ] Documentação de integração

---

### **SPRINT 16: Testes de Carga e Performance** (7 dias)
**Objetivo**: Garantir performance sob carga

#### Entregáveis:
- [ ] Testes de carga (Locust/K6)
- [ ] Cenários:
  - 1000 câmeras simultâneas
  - 100 usuários simultâneos
  - 10.000 eventos LPR/hora
- [ ] Otimizações identificadas
- [ ] Relatório de performance
- [ ] Documentação

---

### **SPRINT 17: Terraform - IaC AWS** (7 dias)
**Objetivo**: Infraestrutura como código para deploy AWS

#### Entregáveis:
- [ ] Terraform modules:
  - VPC, Subnets, Security Groups
  - ECS/EKS (containers)
  - RDS (PostgreSQL)
  - ElastiCache (Redis)
  - S3 (gravações, clipes)
  - CloudFront (CDN para HLS)
  - ALB (Load Balancer)
  - Route53 (DNS)
- [ ] Ambientes: dev, staging, prod
- [ ] Secrets Manager (credenciais)
- [ ] Documentação

---

### **SPRINT 18: CI/CD Pipeline** (5 dias)
**Objetivo**: Pipeline completo de deploy automatizado

#### Entregáveis:
- [ ] GitHub Actions workflows:
  - Testes (unit, integration, E2E)
  - Linting (black, flake8, mypy)
  - Security scan (Bandit, Safety)
  - Build Docker images
  - Push to ECR
  - Deploy to ECS/EKS (Terraform)
- [ ] Rollback automático
- [ ] Notificações (Slack/Discord)
- [ ] Documentação

---

### **SPRINT 19: Documentação Final** (5 dias)
**Objetivo**: Documentação completa do sistema

#### Entregáveis:
- [ ] README principal
- [ ] Guia de instalação (local + AWS)
- [ ] Guia de desenvolvimento
- [ ] Documentação de API (OpenAPI/Swagger)
- [ ] Diagramas de arquitetura (C4 Model)
- [ ] Runbooks (operação)
- [ ] Troubleshooting guide
- [ ] ADRs (Architecture Decision Records)

---

### **SPRINT 20: Testes Finais e Homologação** (7 dias)
**Objetivo**: Validação completa do sistema

#### Entregáveis:
- [ ] Testes de aceitação (UAT)
- [ ] Testes de segurança (OWASP ZAP)
- [ ] Testes de caos (Chaos Monkey)
- [ ] Testes de recuperação de desastres
- [ ] Correção de bugs críticos
- [ ] Relatório final de qualidade

---

## 📊 Métricas de Qualidade

### Cobertura de Testes
- **Unitários**: > 90%
- **Integração**: > 80%
- **E2E**: Fluxos críticos

### Complexidade Ciclomática
- **Máximo por função**: 10
- **Média do projeto**: < 5

### Qualidade de Código
- **Maintainability Index**: > 70
- **Code Smells**: 0 críticos
- **Duplicação**: < 3%

### Performance
- **Latência streaming**: < 500ms
- **API response time**: < 200ms (p95)
- **Uptime**: > 99.9%

---

## 🏗️ Arquitetura DDD

### Camadas por Bounded Context

```
bounded_context/
├── domain/
│   ├── aggregates/
│   ├── entities/
│   ├── value_objects/
│   ├── domain_events/
│   ├── repositories/ (interfaces)
│   └── services/
├── application/
│   ├── use_cases/
│   ├── dtos/
│   ├── event_handlers/
│   └── services/
├── infrastructure/
│   ├── persistence/
│   ├── messaging/
│   ├── external_services/
│   └── web/ (FastAPI/Django)
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

---

## 🔒 Segurança (OWASP Top 10)

1. **Broken Access Control**: RBAC + JWT
2. **Cryptographic Failures**: HTTPS + encryption at rest
3. **Injection**: Prepared statements + sanitização
4. **Insecure Design**: Threat modeling + ADRs
5. **Security Misconfiguration**: Hardening + secrets management
6. **Vulnerable Components**: Dependabot + audits
7. **Authentication Failures**: MFA + rate limiting
8. **Software Integrity Failures**: Signed images + SBOM
9. **Logging Failures**: Centralized logging + SIEM
10. **SSRF**: Whitelist + network segmentation

---

## 📅 Timeline Total

**Duração estimada**: 20 sprints = ~140 dias úteis (~7 meses)

**Fases**:
1. **Fundação** (Sprint 0): 5 dias
2. **Core Backend** (Sprints 1-3): 21 dias
3. **Streaming** (Sprints 4-9): 54 dias
4. **AI** (Sprints 10-11): 12 dias
5. **Observabilidade** (Sprints 12-14): 15 dias
6. **Integração** (Sprint 15): 7 dias
7. **Performance** (Sprint 16): 7 dias
8. **Deploy** (Sprints 17-18): 12 dias
9. **Finalização** (Sprints 19-20): 12 dias

---

## 🚀 Próximos Passos

1. **Revisar e aprovar** este plano de sprints
2. **Iniciar Sprint 0**: Fundação e arquitetura
3. **Setup do ambiente de desenvolvimento**
4. **Primeira reunião de planning**

---

**Última atualização**: 2025-01-16
**Versão**: 2.0
**Progresso**: 70% (14 de 20 sprints completas)
