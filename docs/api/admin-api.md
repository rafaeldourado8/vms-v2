# Admin API Documentation

## 🔐 Autenticação

### Login
Obter tokens JWT para autenticação.

**Endpoint**: `POST /api/auth/login/`

**Request**:
```json
{
  "email": "admin@example.com",
  "password": "SecurePass123"
}
```

**Response** (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Errors**:
- 401: Invalid credentials

---

### Refresh Token
Renovar access token usando refresh token.

**Endpoint**: `POST /api/auth/refresh/`

**Request**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response** (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## 👥 Usuários

### Criar Usuário
Criar novo usuário admin.

**Endpoint**: `POST /api/users/`

**Headers**: Nenhum (público)

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "name": "John Doe"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "is_active": true,
  "roles": []
}
```

**Errors**:
- 400: Email already exists
- 400: Invalid email format
- 400: Password too short (min 8 chars)

---

### Atribuir Role
Atribuir role a um usuário.

**Endpoint**: `POST /api/users/{user_id}/roles/`

**Headers**: `Authorization: Bearer {access_token}`

**Request**:
```json
{
  "role_code": "ADMIN"
}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "is_active": true,
  "roles": ["ADMIN"]
}
```

**Errors**:
- 401: Unauthorized
- 404: User not found
- 404: Role not found

---

## 🔑 Roles Disponíveis

### SUPER_ADMIN
- Acesso total ao sistema
- Pode gerenciar todos os usuários
- Pode criar/editar/deletar qualquer recurso

### ADMIN
- Pode gerenciar usuários da sua prefeitura
- Pode gerenciar câmeras
- Pode visualizar relatórios

### VIEWER
- Apenas visualização
- Não pode editar nada
- Acesso limitado

---

## 🛡️ Segurança

### Rate Limiting
- 100 requests/minuto por IP
- Configurado via Kong Gateway

### JWT Tokens
- **Access Token**: 15 minutos
- **Refresh Token**: 24 horas
- Algoritmo: HS256

### Password Policy
- Mínimo 8 caracteres
- Hash: SHA256 com salt

### Login Attempts
- Máximo 5 tentativas
- Bloqueio automático após exceder

---

## 📝 Exemplos de Uso

### Fluxo Completo

```bash
# 1. Criar usuário
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "SecurePass123",
    "name": "Admin User"
  }'

# 2. Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "SecurePass123"
  }'

# 3. Atribuir role (usando access token)
curl -X POST http://localhost:8000/api/users/{user_id}/roles/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "role_code": "ADMIN"
  }'

# 4. Refresh token
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "{refresh_token}"
  }'
```

---

## 🐛 Troubleshooting

### 401 Unauthorized
- Verifique se o token está válido
- Token pode ter expirado (15 min)
- Use refresh token para renovar

### 400 Email already exists
- Email já cadastrado no sistema
- Use outro email

### 400 Password too short
- Senha deve ter no mínimo 8 caracteres

### 404 User/Role not found
- Verifique se o ID está correto
- Verifique se o recurso existe

---

## 📊 Status Codes

- **200**: OK
- **201**: Created
- **400**: Bad Request
- **401**: Unauthorized
- **404**: Not Found
- **500**: Internal Server Error
