from fastapi import FastAPI
from fastapi import APIRouter
import os

app = FastAPI()
router = APIRouter()

@app.get("/")
def read_root():
    return {"message": "Health OK"}

@router.get("/debug")
async def debug():
    return {
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "SECRET_KEY": os.getenv("SECRET_KEY")
    }
