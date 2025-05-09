from fastapi import FastAPI
from databases import Database
import os
print("🔍 Lanzando test_connection app")

app = FastAPI()

# Leer la variable del entorno (sin .env, directamente del entorno del contenedor)
DATABASE_URL = os.getenv("DATABASE_URL")
database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    try:
        await database.connect()
        print("✅ Conectado a la base de datos")
    except Exception as e:
        print("❌ Error al conectar:", e)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/ping-db")
async def ping_db():
    try:
        row = await database.fetch_one("SELECT NOW();")
        return {"success": True, "timestamp": str(row[0])}
    except Exception as e:
        return {"success": False, "error": str(e)}
