# app/reset_database_alternativo.py

from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from app.db.models import metadata
from sqlalchemy.exc import OperationalError

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

    print("⚙️ Borrando tablas existentes si existen...")
    try:
        with engine.begin() as conn:
            conn.execute(text("DROP TABLE IF EXISTS transport_jobs CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS bikes CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
        print("✅ Tablas eliminadas (si existían).")
    except Exception as e:
        print("❌ Error al eliminar tablas:", e)
        return

    print("⚙️ Creando tablas nuevas...")
    try:
        metadata.create_all(bind=engine)
        print("🎉 Tablas recreadas correctamente.")
    except Exception as e:
        print("❌ Error al crear tablas:", e)

if __name__ == "__main__":
    main()
