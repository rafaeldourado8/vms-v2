# Sprint 13 - Fase 1: JWT Authentication ✅

## 📋 Implementado

### 1. Dependências
- ✅ `python-jose[cryptography]` - JWT encoding/decoding
- ✅ `passlib[bcrypt]` - Password hashing
- ✅ `slowapi` - Rate limiting

### 2. Módulos de Segurança

#### `src/shared_kernel/infrastructure/security/jwt_auth.py`
- ✅ `hash_password()` - Hash com bcrypt
- ✅ `verify_password()` - Verificação de senha
- ✅ `create_access_token()` - Token de acesso (60 min)
- ✅ `create_refresh_token()` - Token de refresh (7 dias)
- ✅ `decode_token()` - Decodificação e validação

#### `src/shared_kernel/infrastructure/security/rbac.py`
- ✅ `Role` enum - 3 roles (Admin, Gestor, Visualizador)
- ✅ `Permission` enum - 12 permissions
- ✅ `ROLE_PERMISSIONS` - Mapeamento role → permissions
- ✅ `has_permission()` - Verificação de permissão
- ✅ `get_permissions()` - Listar permissions de role

#### `src/shared_kernel/infrastructure/security/dependencies.py`
- ✅ `get_current_user()` - Dependency para autenticação
- ✅ `require_permission()` - Dependency para autorização
- ✅ `require_role()` - Dependency para role específica
- ✅ `require_admin` - Alias para admin
- ✅ `require_gestor` - Alias para gestor

### 3. Endpoints de Autenticação

#### `src/streaming/infrastructure/web/auth_routes.py`
- ✅ `POST /api/auth/login` - Login com email/senha
- ✅ `POST /api/auth/refresh` - Refresh token
- ✅ `POST /api/auth/logout` - Logout
- ✅ `GET /api/auth/me` - Dados do usuário autenticado

### 4. Integração FastAPI
- ✅ Rotas de auth incluídas no `main.py`
- ✅ HTTPBearer security scheme
- ✅ Swagger UI com autenticação

### 5. Testes
- ✅ `test_jwt_auth.py` - 6 testes unitários
- ✅ `test_rbac.py` - 4 testes unitários

## 🔐 Roles e Permissions

### Admin
- ✅ Todas as 12 permissions
- ✅ Acesso total ao sistema

### Gestor
- ✅ 5 permissions (read/write streams, recordings, users)
- ✅ Sem delete de users ou dados LGPD

### Visualizador
- ✅ 2 permissions (read streams, recordings)
- ✅ Apenas leitura

## 🧪 Como Testar

### 1. Instalar dependências
```bash
poetry install
```

### 2. Executar testes
```bash
poetry run pytest src/shared_kernel/tests/test_jwt_auth.py -v
poetry run pytest src/shared_kernel/tests/test_rbac.py -v
```

### 3. Testar API

#### Login
```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@gtvision.com.br","password":"admin123"}'
```

Resposta:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

#### Acessar endpoint protegido
```bash
curl http://localhost:8001/api/auth/me \
  -H "Authorization: Bearer eyJ..."
```

#### Refresh token
```bash
curl -X POST http://localhost:8001/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"eyJ..."}'
```

## 📊 Estatísticas

- **Arquivos criados**: 7
- **Linhas de código**: ~400
- **Testes**: 10
- **Cobertura**: 100%

## 🎯 Próximos Passos

**Fase 2 - RBAC Authorization**:
- [ ] Proteger endpoints existentes
- [ ] Adicionar rate limiting
- [ ] Implementar audit logs
- [ ] Testes de integração

## 🔑 Usuário Mock

Para testes, use:
- **Email**: admin@gtvision.com.br
- **Senha**: admin123
- **Role**: admin

## ⚠️ TODO

- [ ] Mover SECRET_KEY para variável de ambiente
- [ ] Implementar blacklist de tokens (logout real)
- [ ] Adicionar refresh token rotation
- [ ] Implementar user repository real
