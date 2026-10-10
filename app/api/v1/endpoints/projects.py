from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.db.prisma import db
from app.schemas.projects import ProjectCreate, ProjectUpdate, ProjectResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects&Labs"])

@router.get("/course/{course_id}", response_model=List[ProjectResponse])
async def list_projects_by_course(course_id: str):
    """Lista todos los proyectos pertenecientes a un curso especifico."""
    return await db.projects.find_many(
        where={"courseId": course_id, "status": "enable"}
    )

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate,
    current_user = Depends(get_current_user)
):

    """Crea un nuevo proyecto/laboratorio dentro de un curso"""
    course = await db.course.find_unique(where={"id":payload.courseId})
    if not course:
        raise HTTPException(status_code=404, detail="El curso especificado no existe")
    return await db.projects.create(
        data={
            "name": payload.nombre,
            "description": payload.description,
            "courseId": payload.courseId
        }
    )

@router.get("/{project_id}",response_model=ProjectResponse)
async def get_project(project_id: str):
    """Obtiene el detalle de un proyecto"""
    project = await db.projects.find_unique(where={"id": project_id})
    if not project or project.status == "disable":
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    payload: ProjectUpdate,
    current_user = Depends(get_current_user)
):
    """Actualiza la información de un proyecto."""
    project = await db.projects.find_unique(where={"id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    return await db.projects.update(where={"id": project_id},data=update_data)

@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    current_user = Depends(get_current_user)
):
    """Deshabilita un proyecto (Soft Delete)"""
    project = await db.projects.find_unique(where={"id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    await db.projects.update(where={"id": project_id}, data={"status":"disable"})
    return {"message": "Proyecto eliminado correctamente"}