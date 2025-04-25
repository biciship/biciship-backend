# app/drop_recreate_bikes.py

from sqlalchemy import create_engine, text
from app.db.models import bikes
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

with engine.begin() as conn:
    # Drop bikes with CASCADE (forzar eliminar también dependencias)
    conn.execute(text("DROP TABLE IF EXISTS bikes CASCADE;"))
    # Luego recreamos la tabla
    bikes.create(bind=engine)
