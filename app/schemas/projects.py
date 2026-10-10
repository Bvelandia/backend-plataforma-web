from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    courseId: str

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: str
    nombre: str
    description: Optional[str] = None
    courseId: str
    status: str
    createdAt: datetime
    updatedAt: datetime

class Config:
    from_attributes = True