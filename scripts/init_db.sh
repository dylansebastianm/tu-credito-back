#!/bin/bash
# Script para inicializar la base de datos

echo "Ejecutando migraciones..."
python manage.py migrate

echo "Creando superusuario (opcional)..."
python manage.py createsuperuser --noinput --username admin --email admin@example.com || echo "Superusuario ya existe o hay un error"

echo "¡Base de datos inicializada!"
