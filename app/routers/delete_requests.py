from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.db.database import database
from app.db.models import delete_requests
from app.auth.dependencies import require_role

router = APIRouter()

@router.get("/")
async def list_delete_requests(user=Depends(require_role(["admin", "operador"]))):
    query = select(delete_requests)
    return await database.fetch_all(query)
