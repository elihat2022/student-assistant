FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Actualizar pip e instalar virtualenv
RUN pip install --no-cache-dir --upgrade pip

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Exponer el puerto
EXPOSE $PORT

# Comando de inicio usando honcho para manejar múltiples procesos
CMD honcho start
