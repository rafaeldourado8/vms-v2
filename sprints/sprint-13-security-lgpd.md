# Sprint 13 - Segurança e LGPD

**Duração**: 7 dias  
**Objetivo**: Implementar segurança robusta e compliance LGPD  
**Status**: 📋 PLANEJADA

---

## 🎯 Objetivos

### Segurança
- Autenticação JWT
- Autorização RBAC
- Rate limiting
- Input validation
- HTTPS/TLS
- Secrets management

### LGPD
- Consentimento
- Anonimização
- Direito ao esquecimento
- Portabilidade de dados
- Logs de auditoria
- Política de privacidade

---

## 📋 Fases

### Fase 1: Autenticação JWT (2 dias)
- [ ] JWT token generation
- [ ] JWT token validation
- [ ] Refresh tokens
- [ ] Login endpoint
- [ ] Logout endpoint
- [ ] Password hashing (bcrypt)
- [ ] User model
- [ ] Auth middleware

### Fase 2: Autorização RBAC (1 dia)
- [ ] Role model (Admin, Gestor, Visualizador)
- [ ] Permission model
- [ ] RBAC middleware
- [ ] Decorators (@require_role)
- [ ] Endpoint protection

### Fase 3: Segurança API (1 dia)
- [ ] Rate limiting (por IP/usuário)
- [ ] Input validation (Pydantic)
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CORS configurado
- [ ] Security headers

### Fase 4: LGPD Compliance (2 dias)
- [ ] Consentimento (termo de aceite)
- [ ] Anonimização de dados sensíveis
- [ ] Direito ao esquecimento (DELETE user)
- [ ] Portabilidade (export JSON)
- [ ] Logs de auditoria
- [ ] Política de privacidade

### Fase 5: Testes e Documentação (1 dia)
- [ ] Testes de segurança
- [ ] Testes LGPD
- [ ] Documentação de segurança
- [ ] Guia LGPD

---

## 🔐 Autenticação JWT

### Fluxo
```
1. POST /auth/login (email, password)
   → Valida credenciais
   → Gera access_token (15min) + refresh_token (7 dias)
   → Retorna tokens

2. Requisições protegidas
   → Header: Authorization: Bearer {access_token}
   → Middleware valida token
   → Extrai user_id e roles
   → Permite acesso

3. POST /auth/refresh (refresh_token)
   → Valida refresh_token
   → Gera novo access_token
   → Retorna novo token

4. POST /auth/logout
   → Invalida refresh_token
   → Retorna sucesso
```

### Implementação

**User Model**:
```python
class User(Entity):
    email: str
    password_hash: str
    name: str
    role: UserRole  # ADMIN, GESTOR, VISUALIZADOR
    cidade_id: Optional[UUID]
    is_active: bool
    created_at: datetime
```

**JWT Service**:
```python
class JWTService:
    def generate_access_token(user_id: UUID, role: str) -> str
    def generate_refresh_token(user_id: UUID) -> str
    def validate_token(token: str) -> dict
    def decode_token(token: str) -> dict
```

**Auth Middleware**:
```python
async def auth_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(401, "Missing token")
    
    user = jwt_service.validate_token(token)
    request.state.user = user
    return await call_next(request)
```

---

## 🛡️ RBAC (Role-Based Access Control)

### Roles

**ADMIN** (Super Admin):
- Acesso total ao sistema
- Gerenciar prefeituras
- Gerenciar usuários
- Ver todas as câmeras

**GESTOR** (Prefeitura):
- CRUD de câmeras da sua cidade
- CRUD de usuários da sua cidade
- Ver streams/gravações da sua cidade
- Criar clipes/mosaicos

**VISUALIZADOR** (Prefeitura):
- Ver câmeras da sua cidade (read-only)
- Ver streams/gravações da sua cidade
- Ver mosaicos

### Implementação

**Permission Decorator**:
```python
def require_role(*allowed_roles):
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            user = request.state.user
            if user.role not in allowed_roles:
                raise HTTPException(403, "Forbidden")
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator

# Uso
@app.post("/api/cameras")
@require_role("ADMIN", "GESTOR")
async def create_camera(request: Request, dto: CreateCameraDTO):
    ...
```

---

## 🔒 Segurança API

### Rate Limiting

**Implementação**:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/auth/login")
@limiter.limit("5/minute")  # 5 tentativas por minuto
async def login(request: Request, dto: LoginDTO):
    ...
```

### Input Validation

**Pydantic Models**:
```python
class LoginDTO(BaseModel):
    email: EmailStr  # Valida email
    password: str = Field(min_length=8, max_length=100)

class CreateCameraDTO(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    url: HttpUrl  # Valida URL
    cidade_id: UUID
```

### Security Headers

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://gtvision.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response
```

---

## 📜 LGPD Compliance

### 1. Consentimento

**Termo de Aceite**:
```python
class UserConsent(Entity):
    user_id: UUID
    privacy_policy_version: str
    accepted_at: datetime
    ip_address: str
```

**Endpoint**:
```python
@app.post("/api/users/{user_id}/consent")
async def accept_privacy_policy(user_id: UUID, dto: ConsentDTO):
    # Registra consentimento
    consent = UserConsent(
        user_id=user_id,
        privacy_policy_version="1.0",
        accepted_at=datetime.now(),
        ip_address=request.client.host
    )
    await consent_repository.save(consent)
```

### 2. Anonimização

**Dados Sensíveis**:
- Placas de veículos (LPR)
- Imagens de câmeras
- Logs de acesso

**Implementação**:
```python
def anonymize_plate(plate: str) -> str:
    # ABC1234 → ABC****
    return plate[:3] + "****"

def anonymize_image(image_url: str) -> str:
    # Blur faces/plates
    return blur_service.blur_image(image_url)
```

### 3. Direito ao Esquecimento

**Endpoint**:
```python
@app.delete("/api/users/{user_id}/gdpr")
async def delete_user_data(user_id: UUID):
    # 1. Anonimizar dados
    await user_service.anonymize_user(user_id)
    
    # 2. Deletar dados pessoais
    await user_repository.delete(user_id)
    
    # 3. Manter logs auditoria (anonimizados)
    await audit_log.log("USER_DELETED", user_id="ANONYMIZED")
```

### 4. Portabilidade

**Endpoint**:
```python
@app.get("/api/users/{user_id}/export")
async def export_user_data(user_id: UUID):
    data = {
        "user": await user_repository.find_by_id(user_id),
        "cameras": await camera_repository.find_by_user(user_id),
        "mosaics": await mosaic_repository.find_by_user(user_id),
        "audit_logs": await audit_log.find_by_user(user_id)
    }
    return JSONResponse(content=data)
```

### 5. Logs de Auditoria

**Audit Log Model**:
```python
class AuditLog(Entity):
    user_id: UUID
    action: str  # LOGIN, CREATE_CAMERA, DELETE_USER
    resource_type: str
    resource_id: UUID
    ip_address: str
    user_agent: str
    timestamp: datetime
```

**Middleware**:
```python
@app.middleware("http")
async def audit_middleware(request: Request, call_next):
    response = await call_next(request)
    
    if request.method in ["POST", "PUT", "DELETE"]:
        await audit_log.log(
            user_id=request.state.user.id,
            action=f"{request.method}_{request.url.path}",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
    
    return response
```

---

## 🧪 Testes

### Testes de Segurança
- [ ] test_login_success
- [ ] test_login_invalid_credentials
- [ ] test_login_rate_limit
- [ ] test_jwt_token_valid
- [ ] test_jwt_token_expired
- [ ] test_jwt_token_invalid
- [ ] test_protected_endpoint_without_token
- [ ] test_protected_endpoint_with_token
- [ ] test_rbac_admin_access
- [ ] test_rbac_gestor_access
- [ ] test_rbac_visualizador_access
- [ ] test_rbac_forbidden

### Testes LGPD
- [ ] test_consent_accept
- [ ] test_anonymize_plate
- [ ] test_delete_user_data
- [ ] test_export_user_data
- [ ] test_audit_log_created

---

## 📊 Checklist

### Segurança
- [ ] JWT implementado
- [ ] RBAC implementado
- [ ] Rate limiting configurado
- [ ] Input validation
- [ ] Security headers
- [ ] Password hashing
- [ ] HTTPS/TLS (produção)

### LGPD
- [ ] Consentimento
- [ ] Anonimização
- [ ] Direito ao esquecimento
- [ ] Portabilidade
- [ ] Logs de auditoria
- [ ] Política de privacidade

### Testes
- [ ] 12 testes de segurança
- [ ] 5 testes LGPD
- [ ] Cobertura >90%

### Documentação
- [ ] Guia de autenticação
- [ ] Guia RBAC
- [ ] Guia LGPD
- [ ] Swagger UI atualizado

---

## 📚 Dependências

```toml
# Segurança
pyjwt = "^2.8"
passlib = "^1.7"
python-multipart = "^0.0.6"
slowapi = "^0.1.9"

# Validação
email-validator = "^2.1"
```

---

## 🎯 Métricas de Sucesso

- ✅ Autenticação JWT funcionando
- ✅ RBAC protegendo endpoints
- ✅ Rate limiting ativo
- ✅ LGPD compliance 100%
- ✅ Testes >90% cobertura
- ✅ Documentação completa

---

**Status**: 📋 Planejamento completo - Pronto para implementação
