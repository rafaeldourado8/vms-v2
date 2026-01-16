# SPRINT 1: Admin Context - Autenticação e Governança (7 dias)

## 🎯 Objetivo
Implementar sistema de autenticação robusto com JWT e gestão de usuários admin.

---

## 📋 Entregáveis

### Domain Layer
- [ ] User aggregate (raiz de agregação)
- [ ] Role entity
- [ ] Permission entity
- [ ] Email value object
- [ ] Password value object
- [ ] UserCreated event
- [ ] UserAuthenticated event
- [ ] IUserRepository interface
- [ ] IRoleRepository interface
- [ ] AuthenticationService (domain service)

### Application Layer
- [ ] CreateUserUseCase
- [ ] AuthenticateUserUseCase
- [ ] AssignRoleUseCase
- [ ] CreateUserDTO
- [ ] AuthenticateDTO
- [ ] UserResponseDTO
- [ ] UserCreatedEventHandler

### Infrastructure Layer
- [ ] UserRepository (PostgreSQL)
- [ ] RoleRepository (PostgreSQL)
- [ ] Django models (User, Role, Permission)
- [ ] JWT authentication backend
- [ ] Django Admin customizado
- [ ] REST API endpoints

### Tests
- [ ] Domain: User aggregate tests
- [ ] Domain: Value objects tests
- [ ] Application: Use cases tests
- [ ] Infrastructure: Repository tests
- [ ] Integration: API tests
- [ ] Cobertura > 90%

---

## 🏗️ Arquitetura

```
admin/
├── domain/
│   ├── aggregates/
│   │   └── user.py
│   ├── entities/
│   │   ├── role.py
│   │   └── permission.py
│   ├── value_objects/
│   │   ├── email.py
│   │   └── password.py
│   ├── events/
│   │   ├── user_created.py
│   │   └── user_authenticated.py
│   ├── repositories/
│   │   ├── user_repository.py
│   │   └── role_repository.py
│   └── services/
│       └── authentication_service.py
├── application/
│   ├── use_cases/
│   │   ├── create_user.py
│   │   ├── authenticate_user.py
│   │   └── assign_role.py
│   ├── dtos/
│   │   ├── create_user_dto.py
│   │   ├── authenticate_dto.py
│   │   └── user_response_dto.py
│   └── event_handlers/
│       └── user_created_handler.py
├── infrastructure/
│   ├── persistence/
│   │   ├── models.py
│   │   ├── user_repository_impl.py
│   │   └── role_repository_impl.py
│   └── web/
│       └── django_app/
│           ├── settings.py
│           ├── urls.py
│           ├── admin.py
│           └── views.py
└── tests/
    ├── unit/
    ├── integration/
    └── fixtures/
```

---

## 📝 Funcionalidades

### 1. Autenticação JWT
- Login com email/password
- Geração de access token (15 min)
- Geração de refresh token (24h)
- Logout (blacklist token)

### 2. Gestão de Usuários
- CRUD de usuários admin
- Ativação/desativação
- Reset de senha
- Auditoria de ações

### 3. RBAC
- Roles: SUPER_ADMIN, ADMIN, VIEWER
- Permissions granulares
- Atribuição de roles
- Verificação de permissões

### 4. Django Admin
- Interface customizada
- Filtros avançados
- Ações em lote
- Logs de auditoria

---

## 🔐 Regras de Negócio

### User Aggregate
1. Email deve ser único
2. Password deve ter mínimo 8 caracteres
3. User deve ter pelo menos 1 role
4. User inativo não pode autenticar
5. Tentativas de login limitadas (5 max)

### Authentication
1. Token expira após 15 minutos
2. Refresh token expira após 24 horas
3. Tokens inválidos são rejeitados
4. Logout invalida todos os tokens do usuário

### Roles & Permissions
1. SUPER_ADMIN tem todas as permissões
2. ADMIN pode gerenciar usuários
3. VIEWER apenas visualiza
4. Permissions são verificadas em cada request

---

## 🧪 Casos de Teste

### Unit Tests
```python
# User aggregate
- test_create_user_with_valid_data()
- test_create_user_with_invalid_email()
- test_create_user_with_weak_password()
- test_user_can_authenticate()
- test_inactive_user_cannot_authenticate()
- test_user_collects_domain_events()

# Value Objects
- test_email_validation()
- test_password_hashing()
- test_password_verification()

# Use Cases
- test_create_user_success()
- test_create_user_duplicate_email()
- test_authenticate_user_success()
- test_authenticate_user_invalid_credentials()
```

### Integration Tests
```python
# API
- test_register_user_endpoint()
- test_login_endpoint()
- test_refresh_token_endpoint()
- test_logout_endpoint()
- test_protected_endpoint_requires_auth()
```

---

## 📊 Métricas de Sucesso

- [ ] Cobertura de testes > 90%
- [ ] Complexidade ciclomática < 10
- [ ] Tempo de resposta login < 200ms
- [ ] Todos os endpoints documentados (OpenAPI)
- [ ] Zero vulnerabilidades (Bandit)

---

## 🚀 Implementação (Dia a Dia)

### Dia 1: Domain Layer - Aggregates & Entities
- User aggregate
- Role entity
- Permission entity
- Testes unitários

### Dia 2: Domain Layer - Value Objects & Events
- Email value object
- Password value object
- Domain events
- Testes unitários

### Dia 3: Domain Layer - Repositories & Services
- Repository interfaces
- Authentication service
- Testes unitários

### Dia 4: Application Layer - Use Cases
- CreateUserUseCase
- AuthenticateUserUseCase
- AssignRoleUseCase
- DTOs
- Testes unitários

### Dia 5: Infrastructure - Persistence
- Django models
- Repository implementations
- Migrations
- Testes de integração

### Dia 6: Infrastructure - Web (API + Admin)
- Django settings
- JWT authentication
- REST API endpoints
- Django Admin customizado
- Testes de integração

### Dia 7: Documentação e Validação
- Documentação OpenAPI
- Testes E2E
- Validação completa
- Deploy em Docker

---

## 🔗 Dependências

### Novas Bibliotecas
```toml
djangorestframework-simplejwt = "^5.3"
django-cors-headers = "^4.3"
argon2-cffi = "^23.1"  # Password hashing
```

### Variáveis de Ambiente
```env
JWT_SECRET_KEY=your-secret-key
JWT_ACCESS_TOKEN_LIFETIME=15
JWT_REFRESH_TOKEN_LIFETIME=1440
```

---

## ✅ Critérios de Aceitação

1. ✅ Usuário pode se registrar com email/password
2. ✅ Usuário pode fazer login e receber JWT
3. ✅ Usuário pode refresh token
4. ✅ Usuário pode fazer logout
5. ✅ Endpoints protegidos requerem autenticação
6. ✅ RBAC funciona corretamente
7. ✅ Django Admin está customizado
8. ✅ Auditoria de ações funciona
9. ✅ Testes > 90% cobertura
10. ✅ Documentação completa

---

**Próxima Sprint**: Sprint 2 - Cidades Context (Gestão de Prefeituras)
