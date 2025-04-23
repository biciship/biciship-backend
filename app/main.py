from fastapi import FastAPI
from app.routers import bikes, users, transport_jobs
from app.db.database import database

app = FastAPI(title="Biciship API")

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(bikes.router, prefix="/bikes", tags=["Bikes"])
app.include_router(transport_jobs.router, prefix="/transport-jobs", tags=["Transport Jobs"])

@app.on_event("startup")
async def startup():
    print("🔥 Iniciando conexión con la base de datos...")
    await database.connect()
    print("✅ Conectado a la base de datos.")

@app.on_event("shutdown")
async def shutdown():
    print("📴 Cerrando conexión con la base de datos...")
    await database.disconnect()
    print("✅ Conexión cerrada.")

@app.get("/")
def root():
    return {"message": "Biciship API funcionando 🚲"}
