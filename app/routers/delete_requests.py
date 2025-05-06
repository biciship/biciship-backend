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

@router.post("/")
async def request_deletion(payload: dict, user=Depends(require_role(["cliente", "transportista"]))):
    resource_type = payload.get("resource_type")  # 'bike' o 'job'
    resource_id = payload.get("resource_id")
    reason = payload.get("reason")

    if resource_type not in ("bike", "job"):
        raise HTTPException(status_code=400, detail="Tipo de recurso inválido")

    if not resource_id or not reason:
        raise HTTPException(status_code=400, detail="Faltan datos requeridos")

    query = insert(delete_requests).values(
        user_id=user["user_id"],
        resource_type=resource_type,
        resource_id=resource_id,
        reason=reason
    )
    req_id = await database.execute(query)
    return {"id": req_id, "message": "Solicitud enviada"}

