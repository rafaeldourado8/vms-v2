# 🚀 PROMPT RÁPIDO - GT-Vision VMS

## Para Assistentes de IA (Cole este prompt)

```
Você está trabalhando no GT-Vision VMS, um sistema VMS (Video Management System) enterprise para prefeituras brasileiras.

CONTEXTO COMPLETO: Leia .context/PROJECT_CONTEXT.md
ESTADO ATUAL: Leia .context/CURRENT_STATE.md
SPRINT ATUAL: Leia sprints/sprint-0.md

ARQUITETURA OBRIGATÓRIA:
- DDD (Domain-Driven Design)
- SOLID
- Monolito Modular
- Bounded Contexts: Admin, Cidades, Streaming, AI

STACK:
- Backend Admin/Cidades: Django 5.0 + DRF
- Backend Streaming/AI: FastAPI
- DB: PostgreSQL 15
- Cache: Redis 7
- Message Broker: RabbitMQ 3
- Streaming: MediaMTX
- Proxy: HAProxy + Kong
- Observabilidade: Prometheus + Grafana + ELK
- Deploy: Docker Compose + Terraform (AWS)

REGRAS CRÍTICAS (NUNCA VIOLAR):
1. Complexidade ciclomática < 10 por função
2. Cobertura de testes > 90%
3. Estrutura DDD: domain/application/infrastructure
4. Domain NUNCA depende de infrastructure
5. Type hints obrigatórios (Python)
6. Código mínimo e funcional
7. SEMPRE escrever testes
8. SEMPRE seguir SOLID

SPRINT ATUAL: Sprint 0 - Fundação e Arquitetura (5 dias)
PROGRESSO: 0% (aguardando início)

PRÓXIMAS TAREFAS:
1. Criar Shared Kernel (base classes DDD)
2. Docker Compose completo
3. Setup de testes (pytest, coverage, mutation)
4. Pre-commit hooks (black, flake8, mypy, isort)
5. ADRs e documentação

ANTES DE FAZER QUALQUER COISA:
- Leia .context/PROJECT_CONTEXT.md (contexto completo)
- Leia .context/CURRENT_STATE.md (estado atual)
- Leia sprints/sprint-0.md (tarefas da sprint)
- Siga RIGOROSAMENTE a arquitetura DDD
- Escreva código MÍNIMO e FUNCIONAL
- SEMPRE escreva testes junto com o código
```

---

## 📋 Checklist Rápido

Antes de começar qualquer tarefa:

- [ ] Li .context/PROJECT_CONTEXT.md?
- [ ] Li .context/CURRENT_STATE.md?
- [ ] Li sprints/sprint-0.md?
- [ ] Entendi a arquitetura DDD?
- [ ] Entendi os bounded contexts?
- [ ] Sei qual sprint estamos?
- [ ] Sei quais tarefas fazer?

---

## 🎯 Comandos Úteis

```bash
# Ver contexto completo
cat .context/PROJECT_CONTEXT.md

# Ver estado atual
cat .context/CURRENT_STATE.md

# Ver sprint atual
cat sprints/sprint-0.md

# Ver planejamento completo
cat sprints/README.md

# Atualizar estado após concluir tarefas
nano .context/CURRENT_STATE.md
```

---

## 💡 Dica para Assistentes

Se você é um assistente de IA e recebeu este projeto:

1. **PARE** e leia os 3 arquivos principais:
   - `.context/PROJECT_CONTEXT.md` (contexto completo)
   - `.context/CURRENT_STATE.md` (estado atual)
   - `sprints/sprint-0.md` (tarefas atuais)

2. **ENTENDA** a arquitetura DDD e os bounded contexts

3. **SIGA** rigorosamente as regras críticas

4. **ESCREVA** código mínimo, funcional e testado

5. **ATUALIZE** o arquivo `.context/CURRENT_STATE.md` após concluir tarefas

---

## 🚨 NUNCA FAÇA ISSO

- ❌ Violar a estrutura DDD
- ❌ Criar código sem testes
- ❌ Ignorar complexidade ciclomática
- ❌ Ignorar type hints
- ❌ Criar código verboso
- ❌ Misturar domain com infrastructure
- ❌ Commitar credenciais
- ❌ Ignorar SOLID

---

## ✅ SEMPRE FAÇA ISSO

- ✅ Seguir DDD rigorosamente
- ✅ Escrever testes (>90% coverage)
- ✅ Manter complexidade < 10
- ✅ Usar type hints
- ✅ Código mínimo e funcional
- ✅ Seguir SOLID
- ✅ Documentar decisões (ADRs)
- ✅ Atualizar CURRENT_STATE.md

---

**Versão**: 1.0
**Última atualização**: 2025-01-XX
