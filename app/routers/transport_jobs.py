from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_jobs():
    return [{"id": 1, "status": "en ruta"}]
