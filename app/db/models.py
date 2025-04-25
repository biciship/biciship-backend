from sqlalchemy import (
    Table, Column, Integer, String, ForeignKey, MetaData, DateTime
)
import datetime

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("email", String, unique=True, nullable=False),
    Column("password", String, nullable=False),  # <-- ESTA LÍNEA NUEVA
    Column("role", String, default="rider"),  # rider, admin, operador...
    Column("created_at", DateTime, default=datetime.datetime.utcnow),
)

bikes = Table(
    "bikes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("model", String, nullable=False),
    Column("status", String, default="available"),  # available, in_use, maintenance
    Column("location", String, nullable=True),
    Column("created_at", DateTime, default=datetime.datetime.utcnow),
)

transport_jobs = Table(
    "transport_jobs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("bike_id", Integer, ForeignKey("bikes.id"), nullable=False),
    Column("origin", String, nullable=False),
    Column("destination", String, nullable=False),
    Column("status", String, default="pending"),  # pending, in_progress, completed
    Column("created_at", DateTime, default=datetime.datetime.utcnow),
)
