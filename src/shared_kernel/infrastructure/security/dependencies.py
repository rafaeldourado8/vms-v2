"""FastAPI Security Dependencies"""
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .jwt_auth import TokenData, decode_token
from .rbac import Permission, Role, has_permission

security = HTTPBearer()


class User:
    """User model for authentication"""
    def __init__(self, user_id: UUID, email: str, role: Role):
        self.id = user_id
        self.email = email
        self.role = role


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> User:
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    token_data = decode_token(token)
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return User(
        user_id=token_data.user_id,
        email=token_data.email,
        role=Role(token_data.role)
    )


def require_permission(permission: Permission):
    """Dependency to require specific permission"""
    async def permission_checker(user: Annotated[User, Depends(get_current_user)]) -> User:
        if not has_permission(user.role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permissão necessária: {permission.value}"
            )
        return user
    return permission_checker


def require_role(role: Role):
    """Dependency to require specific role"""
    async def role_checker(user: Annotated[User, Depends(get_current_user)]) -> User:
        if user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role necessária: {role.value}"
            )
        return user
    return role_checker


# Aliases comuns
require_admin = require_role(Role.ADMIN)
require_gestor = require_role(Role.GESTOR)
