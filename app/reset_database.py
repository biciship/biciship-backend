# app/reset_database.py

from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from app.db.models import metadata

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

with engine.begin() as conn:
    conn.execute(text("DROP SCHEMA public CASCADE;"))
    conn.execute(text("CREATE SCHEMA public;"))
    metadata.create_all(bind=engine)
    print("Base de datos reseteada y recreada correctamente.")
