from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.prisma import connect_db, disconnect_db
from app.api.v1.endpoints import auth, courses, projects, progress, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Conectar a PostgreSQL con Prisma al iniciar el servidor
    await connect_db()
    yield
    #Desconectar Prisma al apagar el servidor
    await disconnect_db()


app = FastAPI(
    title="API Plataforma de Aprendizaje Web",
    version="1.0.0",
    lifespan=lifespan
)

#Configuración de CORS para permitir peticiones desde el Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #Aquí se especifica la URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Inclusión de Routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(courses.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(progress.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "API Backend Plataforma de Aprendizaje funcionando correctamente"}



