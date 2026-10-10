from datetime import datetime, timedelta, timezone
import jwt
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException, status
from app.core.config import settings

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Genera un token JWT firmado por el backend."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY,algorithm=settings.ALGORITHM)

def verify_google_token(token: str) -> dict:
    """Valida el ID Token de Google recibido desde el Frontend."""
    try: 
        id_info = id_token.verify_oauth2_token(
            token, requests.Request(), settings.GOOGLE_CLIENT_ID)
        return id_info
    except ValueError: 
        raise HTTPException( 
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token de Google inválido o expirado")