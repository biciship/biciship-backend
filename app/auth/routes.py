from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import database
from app.db.models import users
from app.auth.utils import hash_password, verify_password, create_access_token
from sqlalchemy import insert, select

router = APIRouter()

# Registro
@router.post("/register")
async def register_user(payload: dict):
    name = payload.get("name")
    email = payload.get("email")
    password = payload.get("password")
    role = payload.get("role") or "cliente"  # 👈 admite rol opcional

    if not name or not email or not password:
        raise HTTPException(status_code=400, detail="Todos los campos son obligatorios")

    query_check = select(users).where(users.c.email == email)
    user_exists = await database.fetch_one(query_check)
    if user_exists:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    hashed_pw = hash_password(password)
    query = insert(users).values(name=name, email=email, password=hashed_pw, role=role)
    await database.execute(query)
    return {"message": "Usuario creado correctamente"}


# Login
@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        print("⏺ Entrando en login")
        query = select(users).where(users.c.email == form_data.username)
        user = await database.fetch_one(query)
        user = dict(user) if user else None

        print(f"Usuario recibido: {form_data.username}")
        print(f"Usuario encontrado: {user['email']}")

        if not user or not verify_password(form_data.password, user["password"]):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        token = create_access_token({
            "sub": user["email"],
            "role": user["role"],
            "user_id": user["id"]
        })
        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        print(f"🔴 ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
