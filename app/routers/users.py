from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import insert, select, delete
from app.db.database import database
from app.db.models import users
from app.auth.dependencies import require_role

router = APIRouter()

@router.get("/")
async def get_users(user=Depends(require_role(["admin", "operador"]))):
    query = select(users)
    return await database.fetch_all(query)

@router.post("/")
async def create_user(payload: dict, user=Depends(require_role(["admin", "operador"]))):
    name = payload.get("name")
    email = payload.get("email")
    role = payload.get("role", "cliente")

    if not name or not email:
        raise HTTPException(status_code=400, detail="Name and email are required")

    query = insert(users).values(name=name, email=email, role=role)
    last_record_id = await database.execute(query)
    return {"id": last_record_id}

@router.delete("/{user_id}")
async def delete_user(user_id: int, user=Depends(require_role(["admin", "operador"]))):
    query = delete(users).where(users.c.id == user_id)
    result = await database.execute(query)
    if result:
        return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")
