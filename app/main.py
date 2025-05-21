from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager

from app.routers import users, bikes, transport_jobs, delete_requests
from app.auth import routes as auth_routes
from app.db.database import database
from app import health

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Iniciando conexión con la base de datos...")
    try:
        await database.connect()
        logging.info("✅ Base de datos conectada correctamente.")
    except Exception as e:
        logging.error(f"❌ Error al conectar con la base de datos: {e}")
        raise e

    yield

    logging.info("Cerrando conexión con la base de datos...")
    try:
        await database.disconnect()
        logging.info("✅ Base de datos desconectada correctamente.")
    except Exception as e:
        logging.warning(f"❌ Error al desconectar la base de datos: {e}")


app = FastAPI(title="Biciship API 🚲", lifespan=lifespan)

# Incluir rutas después de definir `app`
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(bikes.router, prefix="/bikes", tags=["Bikes"])
app.include_router(transport_jobs.router, prefix="/transport-jobs", tags=["Transport Jobs"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(delete_requests.router, prefix="/delete-requests", tags=["Delete Requests"])
app.include_router(health.router)

@app.get("/")
def root():
    logging.info("Endpoint raíz (/) funcionando correctamente.")
    return {"message": "Biciship API funcionando 🚲"}
