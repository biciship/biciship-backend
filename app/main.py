from fastapi import FastAPI
from app.routers import bikes, users, transport_jobs
from app.db.database import database

app = FastAPI(title="Biciship API")

# Rutas
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(bikes.router, prefix="/bikes", tags=["Bikes"])
app.include_router(transport_jobs.router, prefix="/transport-jobs", tags=["Transport Jobs"])

# Eventos de conexión a base de datos
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Ruta raíz
@app.get("/")
def root():
    return {"message": "Biciship API funcionando 🚲"}

# Punto de entrada para ejecución directa
if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
