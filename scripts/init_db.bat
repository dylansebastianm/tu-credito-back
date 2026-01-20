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
echo Creando superusuario (opcional)...
python manage.py createsuperuser --noinput --username admin --email admin@example.com 2>nul || echo Superusuario ya existe o hay un error

echo.
echo ========================================
echo ¡Base de datos inicializada!
echo ========================================
