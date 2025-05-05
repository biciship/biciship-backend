from fastapi import APIRouter, HTTPException
from app.db.database import database
from app.db.models import transport_jobs
from sqlalchemy import insert, select, delete
from app.auth.dependencies import get_current_user
from app.auth.dependencies import require_role


@router.post("/")
async def create_job(payload: dict, user=Depends(get_current_user)):
    ...
    query = insert(transport_jobs).values(
        client_id=user["user_id"],
        bike_id=payload["bike_id"],
        origin=payload["origin"],
        destination=payload["destination"],
        status=payload.get("status", "pending"),
        assigned_to_id=None  # opcional
    )


router = APIRouter()

@router.get("/")
async def get_jobs():
    query = select(transport_jobs)
    return await database.fetch_all(query)

@router.post("/")
async def create_job(payload: dict, user=Depends(get_current_user)):
    query = insert(transport_jobs).values(
        user_id=payload["user_id"],
        bike_id=payload["bike_id"],
        origin=payload["origin"],
        destination=payload["destination"],
        status=payload.get("status", "pending")
    )
    last_record_id = await database.execute(query)
    return {"id": last_record_id}

@router.delete("/{job_id}")
async def delete_job(
    job_id: int,
    dep=Depends(require_role(["admin", "operador"]))):
    query = delete(transport_jobs).where(transport_jobs.c.id == job_id)
    result = await database.execute(query)
    if result:
        return {"message": "Job deleted"}
    raise HTTPException(status_code=404, detail="Job not found")
