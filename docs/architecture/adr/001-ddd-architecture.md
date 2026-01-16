# ADR 001: Arquitetura DDD + Monolito Modular

## Status
Aceito

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
1. **Admin** - Autenticação, governança, usuários admin
2. **Cidades** - Prefeituras, câmeras, planos
3. **Streaming** - Ingestão RTSP, HLS/WebRTC, gravação
4. **AI** - Eventos LPR, busca, análise

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
- Comunicação entre contexts via eventos

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
