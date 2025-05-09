from fastapi import FastAPI
import logging
import os

from app.routers import users, bikes, transport_jobs, delete_requests
from app.auth import routes as auth_routes
from app.db.database import database
from app import health


app = FastAPI(title="Biciship API")  # 👈 esta línea debe ir antes que los includes

# Incluir rutas después de definir `app`
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(bikes.router, prefix="/bikes", tags=["Bikes"])
app.include_router(transport_jobs.router, prefix="/transport-jobs", tags=["Transport Jobs"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(delete_requests.router, prefix="/delete-requests", tags=["Delete Requests"])
#app.include_router(health.router)  # 👈 /debug incluido correctamente

@app.on_event("startup")
async def startup():
    try:
        await database.connect()
    except Exception as e:
        logging.error(f"Error al conectar con la base de datos: {e}")

@app.on_event("shutdown")
async def shutdown():
    try:
        await database.disconnect()
    except Exception as e:
        logging.warning(f"Error al cerrar la conexión: {e}")

@app.get("/")
def root():
    return {"message": "Biciship API funcionando 🚲"}

#@app.get("/debug-db-url")
#def debug_db_url():
#    return {
#        "DATABASE_URL": os.getenv("DATABASE_URL"),
#        "EXISTE_CLOUDSQL_DIR": os.path.exists("/cloudsql")
#    }
