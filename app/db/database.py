from dotenv import load_dotenv
import os
from databases import Database

load_dotenv()  # ✅ esta línea debe ir antes de os.getenv()


DATABASE_URL = os.getenv("DATABASE_URL")
database = Database(DATABASE_URL)
