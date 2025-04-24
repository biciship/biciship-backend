from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import bikes, users, transport_jobs
from app.db.database import database

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(title="Biciship API", lifespan=lifespan)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(bikes.router, prefix="/bikes", tags=["Bikes"])
app.include_router(transport_jobs.router, prefix="/transport-jobs", tags=["Transport Jobs"])

@app.get("/")
def root():
    return {"message": "Biciship API funcionando 🚲"}
