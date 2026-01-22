from fastapi import APIRouter, Header, HTTPException, status
from typing import Optional
import jwt
from datetime import datetime


router = APIRouter(prefix="/auth", tags=["auth"])


SECRET_KEY = "GT_VISION_SECRET_2025"  # TODO: Mover para .env
ALGORITHM = "HS256"


@router.get("/validate", status_code=200)
async def validate_token(
    authorization: Optional[str] = Header(None),
    x_original_uri: Optional[str] = Header(None)
):
    """
    Valida token JWT para auth_request do Nginx.
    
    Retorna:
        200: Token válido
        401: Token inválido/expirado
        403: Sem permissão para o recurso
    """
    
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header"
        )
    
    try:
        # Extrair token
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme"
            )
        
        # Validar JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Verificar expiração
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        
        # TODO: Validar permissões específicas baseado em x_original_uri
        # Exemplo: verificar se tenant_id do token tem acesso à câmera
        
        return {"status": "valid", "user_id": payload.get("sub")}
        
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )
