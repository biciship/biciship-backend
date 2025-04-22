
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_jobs():
    return {"message": "Listar transportes (placeholder)"}
