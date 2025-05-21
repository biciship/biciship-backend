from fastapi import FastAPI
import logging
import os
from app.routers import users, bikes, transport_jobs, delete_requests
from app.auth import routes as auth_routes
from app.db.database import database
from app import health

app = FastAPI(title="Biciship API 🚲")

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(bikes.router, prefix="/bikes", tags=["Bikes"])
app.include_router(transport_jobs.router, prefix="/transport-jobs", tags=["Transport Jobs"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(delete_requests.router, prefix="/delete-requests", tags=["Delete Requests"])
app.include_router(health.router)

@app.on_event("startup")
async def startup():
    try:
        await database.connect()
        logging.info("✅ Database connected (startup event)")
    except Exception as e:
        logging.error(f"❌ Database connection failed (startup event): {e}")

@app.on_event("shutdown")
async def shutdown():
    try:
        await database.disconnect()
        logging.info("✅ Database disconnected (shutdown event)")
    except Exception as e:
        logging.warning(f"❌ Database disconnection failed (shutdown event): {e}")

@app.get("/")
async def root():
    return {"message": "Biciship API funcionando 🚲"}

@app.get("/debug-cloudsql")
async def debug_cloudsql():
    exists = os.path.exists("/cloudsql")
    files = os.listdir("/cloudsql") if exists else []
    logging.info(f"cloudsql_exists: {exists}, cloudsql_files: {files}")
    return {"cloudsql_exists": exists, "cloudsql_files": files}
