from pydantic import BaseModel, EmailStr

class GoogleAuthRequest(BaseModel):
    token: str # ID Token obtenido desde Google OAuth en el Frontend

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict