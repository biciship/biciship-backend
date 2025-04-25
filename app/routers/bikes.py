from fastapi import APIRouter, HTTPException
from app.db.database import database
from app.db.models import bikes
from sqlalchemy import insert, select, delete

router = APIRouter()

@router.get("/")
async def get_bikes():
    query = select(bikes)
    return await database.fetch_all(query)

@router.post("/")
async def create_bike(payload: dict):
    query = insert(bikes).values(model=payload["model"], status=payload.get("status", "available"), location=payload.get("location"))
    last_record_id = await database.execute(query)
    return {"id": last_record_id}

@router.delete("/{bike_id}")
async def delete_bike(bike_id: int):
    query = delete(bikes).where(bikes.c.id == bike_id)
    result = await database.execute(query)
    if result:
        return {"message": "Bike deleted"}
    raise HTTPException(status_code=404, detail="Bike not found")
