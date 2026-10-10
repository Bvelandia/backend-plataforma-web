from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.db.prisma import db
from app.schemas.progress import ProgressCreate, ProgressUpdate, ProgressResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/progress", tags=["CourseProgress"])

@router.get("/me", response_model=List[ProgressResponse])
async def get_my_progress(current_user = Depends(get_current_user)):
    """Obtiene el progreso de todos los cursos asignados al usuario autenticado"""
    return await db.usercourseprogress.find_many(
        where={"userId": current_user.id}
    )

@router.post("/", response_model=ProgressResponse,
             status_code=status.HTTP_201_CREATED)
async def init_course_progress (
    payload: ProgressCreate,
    current_user = Depends(get_current_user)
):
    """Incializa el registro de progreso de un usuario en un curso."""
    existing = await db.usercourseprogress.find_unique(
        where={
            "userId_courseId": {
                "userId": current_user.id,
                "courseId": payload.courseId
            }
        }
    )
    if existing:
        return existing

    return await db.usercourseprogress.create(
        data={
            "userId":current_user.id,
            "courseId": payload.courseId,
            "status": "initialized",
            "percentage": 0.0,
            "hoursdedicated":0.0
        }
    )

@router.put("/{progress_id}", response_model=ProgressResponse)
async def update_progress(
    progress_id : str,
    payload: ProgressUpdate,
    current_user = Depends(get_current_user)
):
    """Actualiza las horas acumuladas, porcentaje o estado de avance."""
    progress = await db.usercourseprogress.find_unique(where={"id": progress_id})
    if not progress:
        raise HTTPException(status_code=404, detail="Registro de progreso no encontrado")
    if progress.userId != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar este registro")
    
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}

    return await db.usercourseprogress.update(where={"id": progress_id},
                                              data=update_data)