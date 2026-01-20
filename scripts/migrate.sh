#!/bin/bash
# Script para ejecutar migraciones de Django en Linux/Mac
# Uso: ./migrate.sh [app_name]
# Si no se especifica app_name, ejecuta todas las migraciones

echo "========================================"
echo "Ejecutando migraciones de Django"
echo "========================================"
echo ""

# Activar entorno virtual si existe
if [ -f "venv/bin/activate" ]; then
    echo "Activando entorno virtual..."
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    echo "Activando entorno virtual..."
    source .venv/bin/activate
else
    echo "Advertencia: No se encontró el entorno virtual"
    echo "Continuando con Python del sistema..."
fi

echo ""
echo "Ejecutando migraciones..."
echo ""

if [ -z "$1" ]; then
    python manage.py migrate
else
    python manage.py migrate "$1"
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Migraciones ejecutadas exitosamente!"
    echo "========================================"
else
    echo ""
    echo "========================================"
    echo "ERROR: Las migraciones fallaron"
    echo "========================================"
    exit 1
fi
