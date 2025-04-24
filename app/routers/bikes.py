from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_bikes():
    return {"bikes": []}
