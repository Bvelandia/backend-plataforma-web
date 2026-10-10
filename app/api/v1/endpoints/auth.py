from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from app.db.prisma import db
from app.schemas.auth import GoogleAuthRequest, TokenResponse
from app.core.security import verify_google_token, create_access_token
from app.services.email import send_welcome_email, send_login_notification


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
async def google_login(payload: GoogleAuthRequest, background_tasks: BackgroundTasks):
    #1. Verificar el token de google
    google_data = verify_google_token(payload.token)
    email = google_data.get("email")
    name = google_data.get("name", "Usuario")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El token de Google no contiene un correo válido"
        )

    #2. Buscar si el usuario ya existe en la Base de Datos
    user = await db.user.find_unique(where={"email": email})

    #3. Si no existe, crearlo (Registro automático)
    if not user:
        user = await db.user.create(
            data={
                "email":email,
                "name": name,
                "role": "STUDENT"
            }
        )
        #Enviar correo de bienvenida con Resend
        background_tasks.add_task(send_welcome_email,email,name)
    else:
        #Enviar notificación de inicio de sesión
        background_tasks.add_task(send_login_notification, email, name)

    #4. Generar el Token JWT firmado por nuestro backend
    access_token = create_access_token(data={"sub": user.id, "role": user.role})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "nombre": user.name,
            "email": user.email,
            "role": user.role
        }
    }

@router.post("/dev-login", summary="Login de prueba para desarrollo")
async def dev_login(email: str = "admin@test.com"):
    """Genera un token JWT de prueba directamente sin necesidad de Google OAuth."""
    user = await db.user.find_unique(where={"email": email})
    if not user:
        user = await db.user.create(
            data={
                "email": email,
                "name": "Usuario de Prueba",
                "role": "ADMIN"
            }
        )

    access_token = create_access_token(data={"sub": user.id, "role": user.role})
    return {"access_token":access_token, "token_type":"bearer"}