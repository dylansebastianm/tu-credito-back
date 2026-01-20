# Guía de Deploy en Render

Esta guía te ayudará a desplegar el backend de Tu Crédito en Render paso a paso.

## 📋 Pasos Previos

### 1. Preparar los datos iniciales (en desarrollo local)

Antes de hacer el deploy, necesitas exportar los datos que quieres tener en producción:

```bash
cd back

# Activar entorno virtual
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Crear datos de prueba (si aún no los tienes)
python manage.py create_sample_data

# Exportar los datos a fixtures
python manage.py export_data
```

Esto creará archivos JSON en `fixtures/`:
- `fixtures/bancos_data.json`
- `fixtures/clientes_data.json`
- `fixtures/creditos_data.json`

**⚠️ IMPORTANTE:** Asegúrate de subir estos archivos al repositorio:
```bash
git add fixtures/*.json
git commit -m "Add initial data fixtures for production"
git push
```

### 2. Verificar que el código esté listo

- ✅ Todas las migraciones están creadas y funcionan localmente
- ✅ Los fixtures están en el directorio `fixtures/` y están en el repositorio
- ✅ El código está en la rama principal (main/master)

## 🚀 Proceso de Deploy en Render

### Paso 1: Crear Base de Datos PostgreSQL

1. Ve a [Render Dashboard](https://dashboard.render.com/)
2. Haz clic en **"New +"** → **"PostgreSQL"**
3. Configura:
   - **Name**: `tu-credito-db` (o el nombre que prefieras)
   - **Database**: `tu_credito_db` (o el nombre que prefieras)
   - **User**: Se genera automáticamente
   - **Region**: Elige la región más cercana a tus usuarios
   - **PostgreSQL Version**: 13 o superior
   - **Plan**: Elige según tus necesidades (Free tier disponible para pruebas)

4. Haz clic en **"Create Database"**

5. **⚠️ IMPORTANTE:** Una vez creada, copia la **Internal Database URL** (la que empieza con `postgresql://`). La necesitarás para el siguiente paso.

### Paso 2: Crear Servicio Web (Django)

1. En Render Dashboard, haz clic en **"New +"** → **"Web Service"**
2. Conecta tu repositorio (GitHub/GitLab/Bitbucket)
3. Selecciona el repositorio y la rama (main/master)
4. Configura el servicio:

   **Basic Settings:**
   - **Name**: `tu-credito-backend` (o el nombre que prefieras)
   - **Region**: Misma región que la base de datos
   - **Branch**: `main` (o la rama que uses)
   - **Root Directory**: `back` (importante: el código Django está en la carpeta `back/`)
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Start Command**: 
     ```bash
     gunicorn tu_credito.wsgi:application --bind 0.0.0.0:$PORT
     ```

   **Environment Variables:**
   Agrega las siguientes variables (haz clic en "Add Environment Variable" para cada una):

   ```
   DJANGO_SETTINGS_MODULE=tu_credito.settings.prod
   SECRET_KEY=<genera-una-clave-secreta-segura>
   DATABASE_URL=<pega-la-internal-database-url-de-paso-1>
   DEBUG=False
   ALLOWED_HOSTS=<nombre-del-servicio>.onrender.com
   JWT_SECRET_KEY=<genera-otra-clave-secreta-para-jwt>
   ```

   **Cómo generar SECRET_KEY y JWT_SECRET_KEY:**
   ```bash
   # En tu terminal local
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Ejecuta esto dos veces para obtener dos claves diferentes.

   **Ejemplo de ALLOWED_HOSTS:**
   Si tu servicio se llama `tu-credito-backend`, será:
   ```
   tu-credito-backend.onrender.com
   ```

5. Haz clic en **"Create Web Service"**

### Paso 3: Configurar Post-Deploy Script (Cargar Datos)

Una vez que el servicio esté creado, necesitas agregar un script para cargar los datos iniciales después del primer deploy:

1. En Render Dashboard, ve a tu servicio web
2. Ve a la pestaña **"Environment"**
3. Agrega una nueva variable de entorno:
   ```
   POST_DEPLOY_COMMAND=python manage.py seed_data --skip-existing
   ```

   **O mejor aún**, crea un archivo `render.yaml` en la raíz del proyecto (no en `back/`) para automatizar todo:

### Paso 4: Crear render.yaml (Opcional pero Recomendado)

Crea un archivo `render.yaml` en la raíz del proyecto con esta configuración:

```yaml
services:
  - type: web
    name: tu-credito-backend
    runtime: python
    buildCommand: pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
    startCommand: gunicorn tu_credito.wsgi:application --bind 0.0.0.0:$PORT
    envVars:
      - key: DJANGO_SETTINGS_MODULE
        value: tu_credito.settings.prod
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: tu-credito-db
          property: connectionString
      - key: DEBUG
        value: False
      - key: ALLOWED_HOSTS
        value: tu-credito-backend.onrender.com
      - key: JWT_SECRET_KEY
        generateValue: true

databases:
  - name: tu-credito-db
    databaseName: tu_credito_db
    user: tu_credito_user
    plan: free
```

**Nota:** Si usas `render.yaml`, Render creará automáticamente la base de datos y el servicio web con esta configuración.

### Paso 5: Instalar gunicorn (si no está en requirements.txt)

Verifica que `gunicorn` esté en `requirements.txt`. Si no está, agrégalo:

```bash
cd back
echo "gunicorn==21.2.0" >> requirements.txt
git add requirements.txt
git commit -m "Add gunicorn for production"
git push
```

### Paso 6: Cargar Datos Iniciales

Después del primer deploy exitoso:

1. Ve a tu servicio web en Render
2. Haz clic en la pestaña **"Shell"** (o usa el botón "Open Shell")
3. Ejecuta:
   ```bash
   python manage.py seed_data --skip-existing
   ```

   O si prefieres hacerlo manualmente:
   ```bash
   python manage.py loaddata fixtures/bancos_data.json
   python manage.py loaddata fixtures/clientes_data.json
   python manage.py loaddata fixtures/creditos_data.json
   ```

### Paso 7: Crear Superusuario

Para poder autenticarte en la API:

1. En la Shell de Render, ejecuta:
   ```bash
   python manage.py createsuperuser
   ```
2. Sigue las instrucciones para crear el usuario
3. **⚠️ IMPORTANTE:** Guarda las credenciales en un gestor seguro (Bitwarden, etc.)

## 🔧 Configuración Adicional

### Variables de Entorno Recomendadas

Además de las básicas, puedes agregar:

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
LOG_LEVEL=INFO
```

### Health Check

Render verificará automáticamente el endpoint `/health/` para saber si el servicio está funcionando.

## ✅ Verificación

Una vez desplegado:

1. **Verifica que el servicio esté corriendo:**
   - Ve a `https://tu-servicio.onrender.com/health/`
   - Deberías ver: `{"status": "ok"}`

2. **Verifica la documentación API:**
   - Ve a `https://tu-servicio.onrender.com/api/docs/`
   - Deberías ver Swagger UI

3. **Verifica que los datos se cargaron:**
   - Obtén un token JWT desde `/api/auth/token/`
   - Haz una petición a `/api/bancos/` con el token
   - Deberías ver los bancos que exportaste

## 🐛 Troubleshooting

### Error: "No module named 'gunicorn'"
- Asegúrate de que `gunicorn` esté en `requirements.txt`

### Error: "Database connection failed"
- Verifica que `DATABASE_URL` esté correctamente configurada
- Asegúrate de usar la **Internal Database URL** (no la externa)

### Error: "Static files not found"
- Verifica que `collectstatic` se ejecute en el build command
- Asegúrate de que `STATIC_ROOT` esté configurado en settings

### Los datos no se cargan
- Verifica que los archivos `fixtures/*.json` estén en el repositorio
- Ejecuta manualmente: `python manage.py seed_data` en la Shell

### Error: "ALLOWED_HOSTS"
- Asegúrate de que `ALLOWED_HOSTS` incluya el dominio de Render (`.onrender.com`)

## 📝 Resumen del Proceso

1. ✅ **Local**: Exportar datos con `python manage.py export_data`
2. ✅ **Git**: Subir fixtures al repositorio
3. ✅ **Render**: Crear base de datos PostgreSQL
4. ✅ **Render**: Crear servicio web Django
5. ✅ **Render**: Configurar variables de entorno
6. ✅ **Render**: Esperar a que el build termine
7. ✅ **Render**: Ejecutar `python manage.py seed_data` en Shell
8. ✅ **Render**: Crear superusuario con `python manage.py createsuperuser`
9. ✅ **Verificar**: Probar endpoints y documentación

## 🔗 URLs Importantes

- **API Base**: `https://tu-servicio.onrender.com/api/`
- **Swagger Docs**: `https://tu-servicio.onrender.com/api/docs/`
- **Health Check**: `https://tu-servicio.onrender.com/health/`
- **Admin (si está habilitado)**: `https://tu-servicio.onrender.com/admin/`

---

**¿Necesitas ayuda?** Revisa los logs en Render Dashboard → Tu Servicio → Logs
