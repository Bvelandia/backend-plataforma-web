import resend
from app.core.config import settings

#Configurar la API Key de Resend desde la configuración global
resend.api_key = settings.RESEND_API_KEY

async def send_welcome_email(user_email: str, user_name: str):
    """Envía un correo de bienvenida tras el registro del usuario."""
    try:
        resend.Emails.send({
            "from": "Plataforma Web <onboarding@resend.dev>",
            "to" : [user_email],
            "subject": "¡Bienvenido a la Plataforma de Aprendizaje!",
            "html": f"<h1>Hola {user_name}</h1><p>Tú registro se ha realizado con éxito. ¡Disfruta tus cursos!</p>"
        })
    except Exception as e:
        print(f'Error enviando correo con Resend: {e}')

async def send_login_notification(user_email: str, user_name: str):
    """Envia una notificación de inicio de sesión seguro."""
    try:
        resend.Emails.send({
            "from": "Plataforma Web <onboarding@resend.dev>",
            "to" : [user_email],
            "subject": "Confirmación de Inicio de Sesión",
            "html": f"<p>Hola {user_name}, detectamos un nuevo inicio de sesión en tú cuenta</p>"
        })
    except Exception as e:
        print(f"Error enviando correo de confirmación de login: {e}")