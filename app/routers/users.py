from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.db.database import database
from app.db.models import users
from app.auth.utils import decode_access_token
from sqlalchemy import insert, select, delete

router = APIRouter()

# Configuración de seguridad OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Función para verificar el token
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

# --- Endpoints ---

@router.get("/", dependencies=[Depends(get_current_user)])
async def get_users():
    query = select(users)
    return await database.fetch_all(query)

@router.post("/")
async def create_user(payload: dict):
    name = payload.get("name")
    email = payload.get("email")
    role = payload.get("role", "rider")  # default si no lo mandan

    if not name or not email:
        raise HTTPException(status_code=400, detail="Name and email are required")

    query = insert(users).values(name=name, email=email, role=role)
    last_record_id = await database.execute(query)
    return {"id": last_record_id}

@router.delete("/{user_id}", dependencies=[Depends(get_current_user)])
async def delete_user(user_id: int):
    query = delete(users).where(users.c.id == user_id)
    result = await database.execute(query)
    if result:
        return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")
