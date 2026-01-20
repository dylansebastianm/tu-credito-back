# Multi-stage build para optimizar tamaño de imagen
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependencias del sistema necesarias para compilación
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim

WORKDIR /app

# Instalar solo runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias instaladas del builder
COPY --from=builder /root/.local /root/.local

# Asegurar que scripts estén en PATH
ENV PATH=/root/.local/bin:$PATH

# Copiar el proyecto
COPY . .

# Crear directorio para logs
RUN mkdir -p /app/logs

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health/')" || exit 1

# Comando por defecto (usar gunicorn en producción)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
