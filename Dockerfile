thFROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY app/ ./app

# Comando de arranque: usar $PORT dinámico que Cloud Run inyecta
CMD exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
