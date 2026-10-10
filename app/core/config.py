from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    RESEND_API_KEY: str
    GOOGLE_CLIENT_ID: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()