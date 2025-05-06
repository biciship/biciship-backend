from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import insert, select, delete
from app.db.database import database
from app.db.models import transport_jobs, bikes, delete_requests
from app.auth.dependencies import require_role

router = APIRouter()

@router.get("/")
async def get_jobs(user=Depends(require_role(["admin", "operador", "cliente", "transportista"]))):
    role = user["role"]
    user_id = user["user_id"]

    if role == "cliente":
        query = select(transport_jobs).where(transport_jobs.c.client_id == user_id)
    elif role == "transportista":
        query = select(transport_jobs).where(transport_jobs.c.assigned_to_id == user_id)
    else:
        query = select(transport_jobs)

    return await database.fetch_all(query)

@router.post("/")
async def create_job(payload: dict, user=Depends(require_role(["admin", "cliente"]))):
    try:
        bike_id = payload.get("bike_id")
        origin = payload.get("origin")
        destination = payload.get("destination")

        if not all([bike_id, origin, destination]):
            raise HTTPException(status_code=400, detail="Faltan campos requeridos")

        bike_query = select(bikes).where(bikes.c.id == bike_id)
        bike = await database.fetch_one(bike_query)
        if not bike:
            raise HTTPException(status_code=404, detail="Bici no encontrada")

        if bike["owner_id"] != user["user_id"] and user["role"] != "admin":
            raise HTTPException(status_code=403, detail="No eres dueño de esta bici")

        query = insert(transport_jobs).values(
            bike_id=bike_id,
            origin=origin,
            destination=destination,
            status="pending",
            client_id=user["user_id"]
        )
        job_id = await database.execute(query)
        return {"id": job_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando trabajo: {str(e)}")

@router.delete("/{job_id}")
async def delete_job(job_id: int, dep=Depends(require_role(["admin", "operador"]))):
    query = delete(transport_jobs).where(transport_jobs.c.id == job_id)
    result = await database.execute(query)
    if result:
        return {"message": "Trabajo eliminado"}
    raise HTTPException(status_code=404, detail="Trabajo no encontrado")

@router.post("/{job_id}/delete-request")
async def request_delete_job(job_id: int, payload: dict, user=Depends(require_role(["cliente", "transportista"]))):
    reason = payload.get("reason")
    if not reason:
        raise HTTPException(status_code=400, detail="Se requiere un motivo para solicitar el borrado.")

    query = insert(delete_requests).values(
        user_id=user["user_id"],
        resource_type="job",
        resource_id=job_id,
        reason=reason
    )
    await database.execute(query)
    return {"message": "Solicitud de borrado registrada"}

