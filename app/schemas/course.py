from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CourseCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CourseUpdate(BaseModel):
    name: str
    description: Optional[str] = None

class CourseResponse(BaseModel):
    id:   str
    name: str
    description: Optional[str] = None
    status: str
    createdAt: datetime
    updatedAt: datetime

class Config:
    from_attributes = True

