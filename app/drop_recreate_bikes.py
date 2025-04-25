# app/drop_recreate_bikes.py

from sqlalchemy import create_engine
from app.db.models import bikes, metadata
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# DROP y CREATE de bikes
with engine.begin() as conn:
    bikes.drop(bind=engine, checkfirst=True)
    bikes.create(bind=engine)
