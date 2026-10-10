from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.db.prisma import db
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/course", tags=["Courses"])

@router.get("/", response_model=List[CourseResponse])
async def list_courses():
    """Obtiene una lista de cursos activos."""
    return await db.course.find_many(where={"status": "enable"})

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    payload: CourseCreate,
    current_user = Depends(get_current_user)
):
    """Crea un nuevo curso (requiere autenticación)"""
    return await db.course.create(
        data={
            "name" : payload.name,
            "description" : payload.description
        }
    )

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: str):
    """Obtiene el detalle de un curso por su ID"""
    course = await db.course.find_unique(where={"id": course_id})
    if not course or course.status == 'disable':
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return course

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: str,
    payload: CourseUpdate,
    current_user = Depends(get_current_user)
):

    """Actualiza la información de un curso"""
    course = await db.course.find_unique(where={"id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    return await db.course.update(where={"id": course_id},
    data=update_data)


@router.delete("/{course_id}")
async def delete_course(
    course_id: str,
    current_user = Depends(get_current_user)
):

    "Deshabilita un curso (Soft Delete)."
    course = await db.course.find_unique(where={"id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    await db.course.update(where={"id": course_id}, data={"status":"disable"})
    return {"message": "Curso eliminado correctamente"}
