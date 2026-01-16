# 6️⃣ Segurança

Medidas técnicas e organizacionais para proteção de dados (Art. 46 da LGPD).

## 🔐 Medidas Técnicas

### 1. Criptografia

#### Em Trânsito (TLS 1.3)
```python
# FastAPI com HTTPS
import uvicorn

uvicorn.run(
    app,
    host="0.0.0.0",
    port=8001,
    ssl_keyfile="/path/to/key.pem",
    ssl_certfile="/path/to/cert.pem",
    ssl_version=ssl.PROTOCOL_TLSv1_3
)
```

#### Em Repouso (AES-256)
```python
from cryptography.fernet import Fernet

class DataEncryption:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted: str) -> str:
        return self.cipher.decrypt(encrypted.encode()).decode()

# Uso
encryption = DataEncryption(settings.ENCRYPTION_KEY)
encrypted_cpf = encryption.encrypt("123.456.789-00")
```

#### Senhas (bcrypt)
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

### 2. Autenticação e Autorização

#### JWT
```python
from jose import jwt
from datetime import datetime, timedelta

def create_access_token(user_id: UUID) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
```

#### RBAC
```python
class Role(str, Enum):
    ADMIN = "admin"
    GESTOR = "gestor"
    VISUALIZADOR = "visualizador"

class Permission(str, Enum):
    READ_STREAMS = "read:streams"
    WRITE_STREAMS = "write:streams"
    READ_USERS = "read:users"
    WRITE_USERS = "write:users"
    DELETE_DATA = "delete:data"

ROLE_PERMISSIONS = {
    Role.ADMIN: [
        Permission.READ_STREAMS,
        Permission.WRITE_STREAMS,
        Permission.READ_USERS,
        Permission.WRITE_USERS,
        Permission.DELETE_DATA
    ],
    Role.GESTOR: [
        Permission.READ_STREAMS,
        Permission.WRITE_STREAMS,
        Permission.READ_USERS
    ],
    Role.VISUALIZADOR: [
        Permission.READ_STREAMS
    ]
}

def require_permission(permission: Permission):
    def decorator(func):
        async def wrapper(user: User, *args, **kwargs):
            if permission not in ROLE_PERMISSIONS[user.role]:
                raise HTTPException(403, "Permissão negada")
            return await func(user, *args, **kwargs)
        return wrapper
    return decorator
```

### 3. Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/auth/login")
@limiter.limit("5/minute")  # 5 tentativas por minuto
async def login(request: Request, credentials: LoginDTO):
    # Login logic
    pass
```

### 4. Input Validation

```python
from pydantic import BaseModel, validator, EmailStr
import re

class CreateUserDTO(BaseModel):
    name: str
    cpf: str
    email: EmailStr
    phone: str
    
    @validator('cpf')
    def validate_cpf(cls, v):
        # Remove formatação
        cpf = re.sub(r'\D', '', v)
        
        # Valida
        if not is_valid_cpf(cpf):
            raise ValueError('CPF inválido')
        
        return cpf
    
    @validator('phone')
    def validate_phone(cls, v):
        phone = re.sub(r'\D', '', v)
        if len(phone) not in [10, 11]:
            raise ValueError('Telefone inválido')
        return phone
```

### 5. SQL Injection Prevention

```python
# ✅ CORRETO - Usar ORM ou prepared statements
from sqlalchemy import select

stmt = select(User).where(User.email == email)
user = session.execute(stmt).scalar_one_or_none()

# ❌ ERRADO - Concatenação de strings
query = f"SELECT * FROM users WHERE email = '{email}'"  # NUNCA FAZER ISSO
```

### 6. XSS Prevention

```python
from fastapi.responses import HTMLResponse
from markupsafe import escape

@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_user_page(user_id: UUID):
    user = User.get(user_id)
    # Escapar dados do usuário
    safe_name = escape(user.name)
    return f"<h1>Usuário: {safe_name}</h1>"
```

### 7. CSRF Protection

```python
from fastapi_csrf_protect import CsrfProtect

@app.post("/api/users")
async def create_user(
    request: Request,
    data: CreateUserDTO,
    csrf_protect: CsrfProtect = Depends()
):
    await csrf_protect.validate_csrf(request)
    # Create user logic
```

### 8. Security Headers

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://gtvision.com.br"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Security headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

### 9. Logs de Auditoria

```python
class AuditLog:
    id: UUID
    user_id: UUID
    action: str  # "LOGIN", "DATA_ACCESS", "DATA_MODIFICATION"
    resource: str  # "User", "Stream", "Recording"
    resource_id: Optional[UUID]
    ip_address: str
    user_agent: str
    timestamp: datetime
    details: dict

def audit_log(action: str):
    def decorator(func):
        async def wrapper(user: User, *args, **kwargs):
            result = await func(user, *args, **kwargs)
            
            # Registrar log
            AuditLog.create(
                user_id=user.id,
                action=action,
                resource=func.__name__,
                timestamp=datetime.now(),
                ip_address=request.client.host,
                user_agent=request.headers.get("user-agent")
            )
            
            return result
        return wrapper
    return decorator

@router.get("/api/users/{user_id}")
@audit_log("DATA_ACCESS")
async def get_user(user_id: UUID, current_user: User):
    return User.get(user_id)
```

### 10. Backup e Recuperação

```bash
# Backup diário automatizado
#!/bin/bash
DATE=$(date +%Y%m%d)
pg_dump -h localhost -U gtvision gtvision_db | gzip > /backups/gtvision_$DATE.sql.gz

# Criptografar backup
gpg --encrypt --recipient dpo@gtvision.com.br /backups/gtvision_$DATE.sql.gz

# Upload para S3
aws s3 cp /backups/gtvision_$DATE.sql.gz.gpg s3://gtvision-backups/
```

## 🏢 Medidas Organizacionais

### 1. Política de Segurança da Informação

**Conteúdo**:
- Classificação de dados
- Controle de acesso
- Gestão de incidentes
- Backup e recuperação
- Treinamento de equipe

### 2. Política de Privacidade

**Conteúdo**:
- Dados coletados
- Finalidades
- Bases legais
- Compartilhamento
- Direitos dos titulares
- Contato do DPO

### 3. Termo de Confidencialidade

```markdown
# Termo de Confidencialidade

Eu, [NOME], [CARGO], declaro estar ciente de que:

1. Tenho acesso a dados pessoais de titulares
2. Devo manter sigilo absoluto sobre esses dados
3. Não posso compartilhar dados sem autorização
4. Devo seguir as políticas de segurança
5. Violações podem resultar em sanções

Data: ___/___/___
Assinatura: _________________
```

### 4. Treinamento de Equipe

**Tópicos**:
- Princípios da LGPD
- Direitos dos titulares
- Bases legais
- Segurança da informação
- Gestão de incidentes
- Boas práticas

**Frequência**: Anual + onboarding

### 5. Avaliação de Impacto (RIPD)

```markdown
# Relatório de Impacto à Proteção de Dados

## 1. Descrição do Tratamento
- Sistema de monitoramento urbano com câmeras e LPR

## 2. Dados Tratados
- Imagens de vias públicas (podem conter biometria)
- Placas de veículos
- Localização e timestamp

## 3. Riscos Identificados
- Reconhecimento facial não autorizado
- Vazamento de dados de localização
- Acesso não autorizado a imagens

## 4. Medidas de Mitigação
- Anonimização de faces
- Criptografia de dados
- Controle de acesso rigoroso
- Logs de auditoria

## 5. Conclusão
- Riscos mitigados adequadamente
- Tratamento necessário para segurança pública
- Conformidade com LGPD
```

### 6. Gestão de Fornecedores

**Checklist**:
- [ ] Cláusula de proteção de dados no contrato
- [ ] Fornecedor é operador (não controlador)
- [ ] Certificações de segurança (ISO 27001)
- [ ] Acordo de confidencialidade
- [ ] Auditoria periódica

### 7. Controle de Acesso Físico

- ✅ Datacenter com acesso restrito
- ✅ Biometria ou cartão de acesso
- ✅ Registro de entrada/saída
- ✅ CFTV no datacenter
- ✅ Destruição segura de mídias

## 📊 Níveis de Segurança

### Nível 1 - Dados Públicos
- Localização de câmeras
- Estatísticas agregadas

**Medidas**: Básicas

### Nível 2 - Dados Pessoais
- Nome, email, telefone
- Logs de acesso

**Medidas**: Criptografia + RBAC + Auditoria

### Nível 3 - Dados Sensíveis
- Imagens com biometria
- Dados de localização

**Medidas**: Todas as anteriores + Anonimização + RIPD

## ✅ Checklist de Segurança

### Técnicas
- [ ] TLS 1.3 em produção
- [ ] Criptografia de dados em repouso
- [ ] Senhas com bcrypt
- [ ] JWT para autenticação
- [ ] RBAC implementado
- [ ] Rate limiting configurado
- [ ] Input validation em todos os endpoints
- [ ] Proteção contra SQL injection
- [ ] Proteção contra XSS
- [ ] CSRF protection
- [ ] Security headers configurados
- [ ] Logs de auditoria
- [ ] Backup diário criptografado

### Organizacionais
- [ ] Política de segurança documentada
- [ ] Política de privacidade publicada
- [ ] Termo de confidencialidade assinado
- [ ] Treinamento anual da equipe
- [ ] RIPD realizado
- [ ] Contratos com fornecedores revisados
- [ ] Controle de acesso físico
- [ ] Plano de resposta a incidentes
