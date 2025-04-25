import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

from app.db.models import metadata

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

if __name__ == "__main__":
    metadata.create_all(engine)
    print("✅ Tablas creadas correctamente.")
