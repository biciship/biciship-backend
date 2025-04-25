from fastapi import APIRouter, HTTPException
from app.db.database import database
from app.db.models import users
from sqlalchemy import insert, select, delete

router = APIRouter()

@router.get("/")
async def get_users():
    query = select(users)
    return await database.fetch_all(query)

@router.post("/")
async def create_user(payload: dict):
    query = insert(users).values(name=payload["name"], email=payload["email"])
    last_record_id = await database.execute(query)
    return {"id": last_record_id}

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    query = delete(users).where(users.c.id == user_id)
    result = await database.execute(query)
    if result:
        return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")
