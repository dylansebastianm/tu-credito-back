#!/bin/bash
# Build script para Render
# Este script se ejecuta automáticamente durante el build

set -o errexit  # Exit on error

echo "🚀 Iniciando build..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones..."
python manage.py migrate --noinput

# Recopilar archivos estáticos
echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ Build completado exitosamente!"
