# app/drop_recreate_users.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from app.db.models import users, metadata

# Cargar variables de entorno
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

# Elimina la tabla users si existe
users.drop(bind=engine, checkfirst=True)

# Crea todas las tablas de nuevo (users)
metadata.create_all(engine)

print("Tabla users eliminada y recreada correctamente.")
