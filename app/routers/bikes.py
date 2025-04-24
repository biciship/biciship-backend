from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_bikes():
    return [{"id": 1, "model": "Road Bike"}]
