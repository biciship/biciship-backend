from fastapi import FastAPI
import logging
import os
from contextlib import asynccontextmanager

from app.routers import users, bikes, transport_jobs, delete_requests
from app.auth import routes as auth_routes
from app.db.database import database
from app import health

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("🔵 Iniciando lifespan, intentando conectar a la DB...")
    try:
        await database.connect()
        logging.info("✅ Conexión inicial a la DB exitosa.")
    except Exception as e:
        logging.error(f"❌ Error crítico al conectar a la DB: {e}")
    yield
    try:
        await database.disconnect()
        logging.info("✅ Desconectado correctamente de la DB.")
    except Exception as e:
        logging.warning(f"❌ Error al desconectar la DB: {e}")

app = FastAPI(title="Biciship API 🚲", lifespan=lifespan)

# Incluir rutas después de definir `app`
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(bikes.router, prefix="/bikes", tags=["Bikes"])
app.include_router(transport_jobs.router, prefix="/transport-jobs", tags=["Transport Jobs"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(delete_requests.router, prefix="/delete-requests", tags=["Delete Requests"])
app.include_router(health.router)

@app.get("/")
async def root():
    logging.info("🔵 Endpoint raíz funcionando.")
    return {"message": "Biciship API funcionando 🚲"}

@app.get("/debug-cloudsql")
async def debug_cloudsql():
    exists = os.path.exists("/cloudsql")
    files = os.listdir("/cloudsql") if
