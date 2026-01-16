# SPRINT 2: Cidades Context - Gestão de Prefeituras (7 dias)

## 🎯 Objetivo
Implementar CRUD completo de prefeituras com planos de armazenamento e gestão de usuários.

---

## 📋 Entregáveis

### Domain Layer
- [ ] Cidade aggregate (raiz de agregação)
- [ ] Plano entity (7/15/30 dias)
- [ ] UsuarioCidade entity
- [ ] CNPJ value object
- [ ] LimiteCameras value object
- [ ] CidadeCriada event
- [ ] PlanoAtribuido event
- [ ] ICidadeRepository interface
- [ ] IPlanoRepository interface

### Application Layer
- [ ] CreateCidadeUseCase
- [ ] UpdateCidadeUseCase
- [ ] AssignPlanoUseCase
- [ ] AddUsuarioCidadeUseCase
- [ ] CreateCidadeDTO
- [ ] UpdateCidadeDTO
- [ ] CidadeResponseDTO
- [ ] PlanoResponseDTO

### Infrastructure Layer
- [ ] CidadeModel (Django)
- [ ] PlanoModel (Django)
- [ ] UsuarioCidadeModel (Django)
- [ ] CidadeRepository implementation
- [ ] PlanoRepository implementation
- [ ] REST API endpoints (CRUD)
- [ ] Django Admin customizado

### Tests
- [ ] Domain tests (>90% coverage)
- [ ] Application tests
- [ ] Integration tests
- [ ] Documentação API

---

## 🏗️ Arquitetura

### Cidade
1. CNPJ deve ser único
2. Nome deve ser único
3. Cidade deve ter 1 plano obrigatório
4. Limite máximo: **1000 câmeras por cidade**
5. Máximo 1 usuário gestor por cidade
6. Máximo 5 usuários visualizadores por cidade

### Plano
1. Tipos: BASICO (7 dias), INTERMEDIARIO (15 dias), AVANCADO (30 dias)
2. Retenção cíclica (sobrescreve após período)
3. Plano não pode ser removido se cidade tiver câmeras

### Usuário Cidade
1. Tipos: GESTOR, VISUALIZADOR
2. Apenas 1 gestor por cidade
3. Máximo 5 visualizadores por cidade
4. Gestor tem CRUD completo
5. Visualizador apenas leitura

---

## 📊 Estrutura

```
cidades/
├── domain/
│   ├── aggregates/
│   │   └── cidade.py
│   ├── entities/
│   │   ├── plano.py
│   │   └── usuario_cidade.py
│   ├── value_objects/
│   │   ├── cnpj.py
│   │   └── limite_cameras.py
│   ├── events/
│   │   ├── cidade_criada.py
│   │   └── plano_atribuido.py
│   └── repositories/
│       ├── cidade_repository.py
│       └── plano_repository.py
├── application/
│   ├── use_cases/
│   │   ├── create_cidade.py
│   │   ├── update_cidade.py
│   │   ├── assign_plano.py
│   │   └── add_usuario_cidade.py
│   └── dtos/
│       ├── create_cidade_dto.py
│       ├── cidade_response_dto.py
│       └── plano_response_dto.py
├── infrastructure/
│   ├── persistence/
│   │   ├── models.py
│   │   ├── cidade_repository_impl.py
│   │   └── plano_repository_impl.py
│   └── web/
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
└── tests/
    └── unit/
```

---

## 🔗 API Endpoints

### Cidades
- `POST /api/cidades/` - Criar cidade
- `GET /api/cidades/` - Listar cidades
- `GET /api/cidades/{id}/` - Obter cidade
- `PUT /api/cidades/{id}/` - Atualizar cidade
- `DELETE /api/cidades/{id}/` - Deletar cidade

### Planos
- `POST /api/cidades/{id}/plano/` - Atribuir plano
- `GET /api/planos/` - Listar planos disponíveis

### Usuários Cidade
- `POST /api/cidades/{id}/usuarios/` - Adicionar usuário
- `GET /api/cidades/{id}/usuarios/` - Listar usuários
- `DELETE /api/cidades/{id}/usuarios/{user_id}/` - Remover usuário

---

## 🧪 Casos de Teste

### Domain
```python
- test_cidade_requires_cnpj()
- test_cidade_requires_plano()
- test_cidade_validates_cnpj_format()
- test_cidade_limite_cameras_max_1000()
- test_cidade_can_add_gestor()
- test_cidade_cannot_add_second_gestor()
- test_cidade_can_add_max_5_visualizadores()
- test_plano_tipos_validos()
```

### Application
```python
- test_create_cidade_success()
- test_create_cidade_duplicate_cnpj()
- test_assign_plano_success()
- test_add_usuario_gestor_success()
- test_add_usuario_gestor_duplicate_fails()
```

---

## 📅 Cronograma

### Dia 1-2: Domain Layer
- Cidade aggregate
- Plano, UsuarioCidade entities
- Value objects (CNPJ, LimiteCameras)
- Domain events
- Testes unitários

### Dia 3-4: Application Layer
- Use cases (Create, Update, Assign)
- DTOs
- Event handlers
- Testes unitários

### Dia 5-6: Infrastructure Layer
- Django models
- Repositories
- REST API
- Django Admin
- Testes integração

### Dia 7: Documentação e Validação
- API documentation
- Testes E2E
- Validação completa
- Relatório final

---

## ✅ Critérios de Aceitação

1. ✅ CRUD completo de cidades
2. ✅ Validação de CNPJ
3. ✅ Planos funcionando (7/15/30 dias)
4. ✅ Gestão de usuários (1 gestor + 5 visualizadores)
5. ✅ Limite de 1000 câmeras validado
6. ✅ Django Admin customizado
7. ✅ Testes >90% cobertura
8. ✅ Documentação completa

---

**Próxima Sprint**: Sprint 3 - Cidades Context (Gestão de Câmeras)
