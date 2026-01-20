# Guía Rápida de Instalación

## Instalación Rápida

### 1. Clonar y entrar al proyecto
```bash
cd "C:\Users\dylan\Desktop\Tu Credito"
```

### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
# Copiar archivo de ejemplo
copy env.example .env

# Editar .env con tus valores (opcional para desarrollo local)
```

### 5. Configurar base de datos PostgreSQL
```bash
# Crear base de datos
createdb tu_credito_db

# O usando psql
psql -U postgres -c "CREATE DATABASE tu_credito_db;"
```

### 6. Ejecutar migraciones
```bash
python manage.py migrate
```

### 7. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 8. Ejecutar servidor
```bash
python manage.py runserver
```

## Con Docker (Recomendado)

```bash
# Copiar variables de entorno
copy env.example .env

# Levantar servicios
docker-compose up --build

# En background
docker-compose up -d
```

El API estará disponible en: `http://localhost:8000`
Documentación: `http://localhost:8000/api/docs/`

## Obtener Token JWT

```bash
POST http://localhost:8000/api/auth/token/
Content-Type: application/json

{
    "username": "tu_usuario",
    "password": "tu_contraseña"
}
```
