# app/reset_database_safe.py

from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
from app.db.models import metadata

def main():
    load_dotenv()

    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("❌ Error: DATABASE_URL no encontrado en .env")
        return

    engine = create_engine(DATABASE_URL)

    print("🔄 Comprobando conexión a la base de datos...")
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ Conexión exitosa a la base de datos.")
    except OperationalError as e:
        print("❌ Error de conexión:", e)
        return

    print("⚙️ Reseteando base de datos...")
    try:
        with engine.begin() as conn:
            conn.execute(text("DROP SCHEMA public CASCADE;"))
            conn.execute(text("CREATE SCHEMA public;"))
            metadata.create_all(bind=engine)
            print("🎉 Base de datos reseteada y recreada correctamente.")
    except Exception as e:
        print("❌ Error durante el reseteo:", e)

if __name__ == "__main__":
    main()
