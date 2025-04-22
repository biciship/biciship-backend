
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_bikes():
    return {"message": "Listar bicicletas (placeholder)"}
