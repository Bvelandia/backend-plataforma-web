from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProgressCreate(BaseModel):
    courseId: str

class ProgressUpdate(BaseModel):
    status: Optional[str] = None
    hoursdedicated: Optional[float] = None
    percentege: Optional[float] = None

class ProgressResponse(BaseModel):
    id: str
    userId: str
    courseId: str
    status: str
    hoursdedicated: float
    percentege: float
    updateAt: datetime

class Config:
    from_attributes = True