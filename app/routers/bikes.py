from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import insert, select, delete
from app.db.database import database
from app.db.models import bikes, delete_requests
from app.auth.dependencies import require_role

router = APIRouter()

@router.get("/")
async def get_bikes(user=Depends(require_role(["admin", "operador", "cliente", "transportista"]))):
    role = user["role"]
    user_id = user["user_id"]

    if role in ["admin", "operador"]:
        query = select(bikes)
    elif role == "cliente":
        query = select(bikes).where(bikes.c.owner_id == user_id)
    else:  # transportista
        # Mostramos solo las bicis asociadas a sus transport_jobs (se podría mejorar con un join en el futuro)
        query = select(bikes)  # simplificado temporalmente
    return await database.fetch_all(query)

@router.post("/")
async def create_bike(payload: dict, user=Depends(require_role(["cliente", "admin"]))):
    try:
        model = payload.get("model")
        status = payload.get("status", "available")
        location = payload.get("location")

        if not model:
            raise HTTPException(status_code=400, detail="Model is required")

        query = insert(bikes).values(
            model=model,
            status=status,
            location=location,
            owner_id=user["user_id"]
        )
        last_record_id = await database.execute(query)
        return {"id": last_record_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating bike: {str(e)}")

@router.delete("/{bike_id}")
async def delete_bike(bike_id: int, dep=Depends(require_role(["admin", "operador"]))):
    query = delete(bikes).where(bikes.c.id == bike_id)
    result = await database.execute(query)
    if result:
        return {"message": "Bike deleted"}
    raise HTTPException(status_code=404, detail="Bike not found")

@router.post("/{bike_id}/delete-request")
async def request_delete_bike(bike_id: int, payload: dict, user=Depends(require_role(["cliente", "transportista"]))):
    reason = payload.get("reason")
    if not reason:
        raise HTTPException(status_code=400, detail="Se requiere un motivo para solicitar el borrado.")

    query = insert(delete_requests).values(
        user_id=user["user_id"],
        resource_type="bike",
        resource_id=bike_id,
        reason=reason
    )
    await database.execute(query)
    return {"message": "Solicitud de borrado registrada"}
