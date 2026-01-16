# Sprint 13 - Fase 2: RBAC & Rate Limiting ✅

## 📋 Implementado

### 1. Proteção de Endpoints com RBAC

#### Endpoints Protegidos
- ✅ `POST /api/streams/start` - Requer `WRITE_STREAMS`
- ✅ `POST /api/streams/{id}/stop` - Requer `WRITE_STREAMS`
- ✅ `GET /api/streams/{id}` - Requer `READ_STREAMS`
- ✅ `POST /api/recordings/start` - Requer `WRITE_RECORDINGS`
- ✅ `POST /api/recordings/{id}/stop` - Requer `WRITE_RECORDINGS`
- ✅ `GET /api/recordings/{id}` - Requer `READ_RECORDINGS`
- ✅ `GET /api/recordings/search` - Requer `READ_RECORDINGS`

#### Endpoints Públicos
- ✅ `POST /api/auth/login` - Público (com rate limit)
- ✅ `POST /api/auth/refresh` - Público
- ✅ `GET /health` - Público
- ✅ `GET /metrics` - Público

### 2. Rate Limiting

#### Configuração
- ✅ `POST /api/auth/login` - 5 requisições/minuto por IP
- ✅ Middleware SlowAPI integrado
- ✅ Handler customizado para erro 429

#### Implementação
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, credentials: LoginRequest):
    ...
```

### 3. Testes de Integração

#### `test_auth_integration.py`
- ✅ `test_protected_endpoint_without_token()` - 403 sem token
- ✅ `test_protected_endpoint_with_invalid_token()` - 401 token inválido
- ✅ `test_login_and_access_protected_endpoint()` - Fluxo completo
- ✅ `test_rate_limit_on_login()` - Rate limit funcionando

## 🔐 Matriz de Permissões

### Admin
- ✅ Acesso total (12 permissions)
- ✅ Pode criar/ler/modificar/deletar tudo

### Gestor
- ✅ 5 permissions
- ✅ Pode criar/ler streams e recordings
- ✅ Pode ler usuários
- ❌ Não pode deletar

### Visualizador
- ✅ 2 permissions
- ✅ Apenas leitura de streams e recordings
- ❌ Não pode modificar nada

## 🧪 Como Testar

### 1. Login como Admin
```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@gtvision.com.br","password":"admin123"}'
```

### 2. Usar token para acessar endpoint protegido
```bash
TOKEN="seu_token_aqui"

curl -X POST http://localhost:8001/api/streams/start \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"camera_id":"123e4567-e89b-12d3-a456-426614174000","source_url":"rtsp://test"}'
```

### 3. Testar sem token (deve falhar)
```bash
curl -X POST http://localhost:8001/api/streams/start \
  -H "Content-Type: application/json" \
  -d '{"camera_id":"123e4567-e89b-12d3-a456-426614174000","source_url":"rtsp://test"}'
```

### 4. Testar rate limit (6+ requisições em 1 minuto)
```bash
for i in {1..6}; do
  curl -X POST http://localhost:8001/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"test@test.com","password":"wrong"}'
  echo ""
done
```

### 5. Executar testes
```bash
poetry run pytest src/streaming/tests/integration/test_auth_integration.py -v
```

## 📊 Estatísticas

- **Endpoints protegidos**: 7
- **Endpoints públicos**: 4
- **Rate limits**: 1 (login)
- **Testes**: 4 integration tests
- **Linhas de código**: ~150

## 🎯 Próximos Passos

**Fase 3 - LGPD Compliance**:
- [ ] Audit logs automáticos
- [ ] Endpoints LGPD (acesso, correção, exclusão, portabilidade)
- [ ] Anonimização de dados
- [ ] Gestão de consentimento
- [ ] Testes E2E

## ⚠️ Notas

- Rate limit usa IP do cliente
- Tokens JWT expiram em 60 minutos
- Refresh tokens expiram em 7 dias
- Todas as rotas protegidas retornam 401 (não autenticado) ou 403 (sem permissão)
