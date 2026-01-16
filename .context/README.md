# 📁 .context - Contexto do Projeto

Esta pasta contém arquivos essenciais para manter a continuidade do projeto GT-Vision VMS em qualquer assistente de IA.

---

## 📄 Arquivos

### 1. PROJECT_CONTEXT.md
**Propósito**: Contexto completo do projeto
**Quando usar**: Sempre que iniciar trabalho no projeto ou precisar entender a arquitetura

**Contém**:
- Visão geral do projeto
- Arquitetura DDD e princípios SOLID
- Stack tecnológica completa
- Requisitos funcionais e não-funcionais
- Estrutura de pastas
- Planejamento de sprints
- Regras críticas (NUNCA VIOLAR)
- Próximos passos

### 2. CURRENT_STATE.md
**Propósito**: Estado atual do projeto e progresso
**Quando usar**: Antes de iniciar qualquer tarefa e após concluir tarefas

**Contém**:
- Sprint atual
- Progresso (% concluído)
- Tarefas concluídas
- Tarefas em andamento
- Próximas tarefas
- Bloqueios
- Métricas de código
- Histórico de atualizações

**IMPORTANTE**: Sempre atualize este arquivo após concluir tarefas!

### 3. QUICK_PROMPT.md
**Propósito**: Prompt rápido para copiar e colar em assistentes de IA
**Quando usar**: Ao iniciar uma nova sessão com um assistente

**Contém**:
- Prompt formatado para copiar/colar
- Checklist rápido
- Comandos úteis
- Regras críticas resumidas

---

## 🚀 Como Usar

### Para Desenvolvedores

1. **Ao iniciar o dia**:
   ```bash
   cat .context/CURRENT_STATE.md
   ```

2. **Ao concluir tarefas**:
   ```bash
   nano .context/CURRENT_STATE.md
   # Marque tarefas como concluídas [x]
   # Atualize progresso
   # Adicione notas se necessário
   ```

3. **Ao mudar de sprint**:
   ```bash
   nano .context/CURRENT_STATE.md
   # Atualize "Sprint Atual"
   # Atualize "Próximas Tarefas"
   # Atualize "Progresso Geral"
   ```

### Para Assistentes de IA

1. **Ao receber o projeto pela primeira vez**:
   ```bash
   # Leia nesta ordem:
   cat .context/QUICK_PROMPT.md      # Prompt rápido
   cat .context/PROJECT_CONTEXT.md   # Contexto completo
   cat .context/CURRENT_STATE.md     # Estado atual
   cat sprints/sprint-0.md           # Sprint atual
   ```

2. **Ao retomar trabalho**:
   ```bash
   cat .context/CURRENT_STATE.md     # Ver estado atual
   cat sprints/sprint-X.md           # Ver tarefas da sprint
   ```

3. **Após concluir tarefas**:
   - Atualize `.context/CURRENT_STATE.md`
   - Marque tarefas como concluídas
   - Adicione notas importantes

---

## 📋 Workflow Recomendado

```
┌─────────────────────────────────────────┐
│ 1. Ler QUICK_PROMPT.md                  │
│    (Entender contexto rápido)           │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ 2. Ler PROJECT_CONTEXT.md              │
│    (Entender arquitetura e regras)      │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ 3. Ler CURRENT_STATE.md                 │
│    (Ver progresso e próximas tarefas)   │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ 4. Ler sprints/sprint-X.md              │
│    (Ver detalhes da sprint atual)       │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ 5. TRABALHAR nas tarefas                │
│    (Seguir DDD, SOLID, testes)          │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ 6. ATUALIZAR CURRENT_STATE.md           │
│    (Marcar tarefas concluídas)          │
└─────────────────────────────────────────┘
```

---

## 🎯 Objetivo

Garantir que **qualquer assistente de IA** possa:
1. Entender o projeto rapidamente
2. Saber exatamente onde estamos
3. Saber o que fazer a seguir
4. Seguir as regras e arquitetura
5. Manter continuidade entre sessões

---

## 🚨 IMPORTANTE

### NUNCA delete ou modifique estes arquivos sem motivo:
- `PROJECT_CONTEXT.md` - Contexto permanente
- `CURRENT_STATE.md` - Estado dinâmico (atualizar sempre)
- `QUICK_PROMPT.md` - Prompt de referência

### SEMPRE atualize:
- `CURRENT_STATE.md` após concluir tarefas
- `CURRENT_STATE.md` ao mudar de sprint
- `CURRENT_STATE.md` ao identificar bloqueios

---

## 📞 Dúvidas?

Se você é um assistente de IA e tem dúvidas:
1. Releia `PROJECT_CONTEXT.md`
2. Verifique `CURRENT_STATE.md`
3. Consulte `sprints/README.md`
4. Consulte `sprints/sprint-X.md` (sprint atual)

---

## 📊 Estrutura de Arquivos

```
.context/
├── README.md              # Este arquivo (explicação)
├── PROJECT_CONTEXT.md     # Contexto completo (permanente)
├── CURRENT_STATE.md       # Estado atual (dinâmico)
└── QUICK_PROMPT.md        # Prompt rápido (referência)
```

---

**Versão**: 1.0
**Última atualização**: 2025-01-XX
**Propósito**: Garantir continuidade do projeto entre sessões e assistentes
