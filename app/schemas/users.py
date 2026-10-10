from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    status: str
    createdAt: datetime

    class Config:
        from_attributes = True