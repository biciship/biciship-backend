
from fastapi import FastAPI
from app.routers import bikes, users, transport_jobs
from app.db.database import database

app = FastAPI(title="Biciship API")

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(bikes.router, prefix="/bikes", tags=["Bikes"])
app.include_router(transport_jobs.router, prefix="/transport-jobs", tags=["Transport Jobs"])

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def root():
    return {"message": "Biciship API funcionando 🚲"}

import os
