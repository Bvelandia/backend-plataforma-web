from fastapi import APIRouter, Depends
from app.schemas.users import UserResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
async def get_profile(current_user = Depends(get_current_user)):
    """Obtiene la información del perfil del usuario actualmente autenticado"""
    return current_user