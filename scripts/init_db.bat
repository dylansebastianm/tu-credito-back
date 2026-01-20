@echo off
REM Script para inicializar la base de datos en Windows

echo ========================================
echo Inicializando base de datos
echo ========================================
echo.

REM Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
)

echo.
echo Ejecutando migraciones...
python manage.py migrate

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Las migraciones fallaron
    exit /b 1
)

echo.
echo ========================================
echo IMPORTANTE: Crear usuario para autenticación
echo ========================================
echo.
echo Para autenticarte en la API, necesitas crear un usuario manualmente:
echo   python manage.py createsuperuser
echo.
echo Este comando te pedirá:
echo   - Username (ej: admin)
echo   - Email (opcional)
echo   - Password (guarda esta contraseña en un gestor seguro como Bitwarden)
echo.
echo Luego usa ese username y password en /api/auth/token/ para obtener el JWT.
echo.

echo.
echo Cargando datos iniciales (si existen fixtures)...
if exist "fixtures\*_data.json" (
    python manage.py seed_data --skip-existing 2>nul || echo No hay fixtures o ya fueron cargados
) else (
    echo No se encontraron fixtures. Para crear datos iniciales:
    echo   1. Crea datos en desarrollo local
    echo   2. Ejecuta: python manage.py export_data
    echo   3. Sube los archivos fixtures/ al repositorio
    echo   4. En producción, ejecuta: python manage.py seed_data
)

echo.
echo ========================================
echo ¡Base de datos inicializada!
echo ========================================
