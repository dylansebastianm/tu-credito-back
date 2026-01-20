@echo off
REM Script para crear y ejecutar migraciones de Django en Windows
REM Uso: migrate.bat [app_name]
REM Si no se especifica app_name, ejecuta todas las migraciones

echo ========================================
echo Creando y ejecutando migraciones de Django
echo ========================================
echo.

REM Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo Advertencia: No se encontró el entorno virtual en venv\Scripts\
    echo Continuando con Python del sistema...
)

echo.
echo Ejecutando migraciones (crea y aplica automáticamente)...
echo.

if "%1"=="" (
    python manage.py migrate_auto
) else (
    python manage.py migrate_auto %1
)

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Migraciones creadas y aplicadas exitosamente!
    echo ========================================
) else (
    echo.
    echo ========================================
    echo ERROR: Las migraciones fallaron
    echo ========================================
    exit /b 1
)
