"""Authentication Endpoints"""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, EmailStr

from src.shared_kernel.infrastructure.security import (
    Token,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from src.shared_kernel.infrastructure.security.dependencies import User, get_current_user
from src.shared_kernel.infrastructure.security.rate_limiter import limiter
from src.shared_kernel.infrastructure.security.audit_log import AuditLog, AuditAction
from src.shared_kernel.infrastructure.logging import elk_logger

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


# Mock user database (substituir por repositório real)
MOCK_USERS = {
    "admin@gtvision.com.br": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "email": "admin@gtvision.com.br",
        "password": "admin123",  # Plain password for testing
        "role": "admin",
        "name": "Administrador"
    }
}


@router.post("/login", response_model=Token)
async def login(request: Request, credentials: LoginRequest):
    """Login com email e senha"""
    user = MOCK_USERS.get(credentials.email)
    
    # Simple password check for testing (use verify_password in production)
    if not user or credentials.password != user["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    access_token = create_access_token(
        user_id=UUID(user["id"]),
        email=user["email"],
        role=user["role"]
    )
    refresh_token = create_refresh_token(user_id=UUID(user["id"]))
    
    # Audit log
    AuditLog.record(
        action=AuditAction.LOGIN,
        user_id=UUID(user["id"]),
        ip_address=request.client.host if request.client else None
    )
    
    # ELK log
    elk_logger.log_security_audit(
        action="LOGIN",
        user_id=UUID(user["id"]),
        ip_address=request.client.host if request.client else None,
        resource="/api/auth/login"
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/refresh", response_model=Token)
async def refresh(request: RefreshRequest):
    """Refresh access token"""
    token_data = decode_token(request.refresh_token)
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido"
        )
    
    # Buscar usuário (mock)
    user = next(
        (u for u in MOCK_USERS.values() if u["id"] == str(token_data.user_id)),
        None
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado"
        )
    
    access_token = create_access_token(
        user_id=token_data.user_id,
        email=user["email"],
        role=user["role"]
    )
    refresh_token = create_refresh_token(user_id=token_data.user_id)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/logout")
async def logout(user: Annotated[User, Depends(get_current_user)]):
    """Logout (invalidar token no cliente)"""
    # Audit log
    AuditLog.record(
        action=AuditAction.LOGOUT,
        user_id=user.id
    )
    
    # ELK log
    elk_logger.log_security_audit(
        action="LOGOUT",
        user_id=user.id,
        resource="/api/auth/logout"
    )
    return {"message": "Logout realizado com sucesso"}


@router.get("/me")
async def get_me(user: Annotated[User, Depends(get_current_user)]):
    """Obter dados do usuário autenticado"""
    return {
        "id": str(user.id),
        "email": user.email,
        "role": user.role.value
    }
