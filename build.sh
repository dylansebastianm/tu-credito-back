#!/bin/bash
# Build script para Render
# Este script se ejecuta automáticamente durante el build

set -o errexit  # Exit on error

echo "🚀 Iniciando build..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Crear y ejecutar migraciones
echo "🗄️ Creando migraciones..."
python manage.py makemigrations --noinput || echo "⚠️ No hay migraciones nuevas para crear"

echo "🗄️ Aplicando migraciones..."
python manage.py migrate --noinput

# Recopilar archivos estáticos
echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Cargar datos iniciales (fixtures)
# Deshabilitar emails durante la carga de datos para acelerar el deploy
echo "📊 Cargando datos iniciales..."
DISABLE_EMAIL_SIGNALS=1 python manage.py seed_data --skip-existing

echo "✅ Build completado exitosamente!"
