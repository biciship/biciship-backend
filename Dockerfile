FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🔧 Copiar el archivo de entorno (asegúrate de que existe)
COPY .env .  # <--- ESTA LÍNEA ES CLAVE

# Copiar el código fuente
COPY . .

# Comando de arranque: usar $PORT dinámico que Cloud Run inyecta
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
