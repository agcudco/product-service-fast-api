from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.init_db import init_db
from app.db.seed import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("🚀 Iniciando Product Service...")

    # Crear tablas
    init_db()

    # Crear datos iniciales
    seed_database()

    print("✅ Product Service inicializado")

    yield

    print("🛑 Cerrando Product Service...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)


@app.get(
    "/health",
    tags=["Health"],
)
def health():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
    }


app.include_router(
    api_router,
    prefix=settings.API_V1_STR,
)