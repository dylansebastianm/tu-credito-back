# Tu Crédito - Backend API

Backend profesional para el sistema de gestión de clientes, créditos y bancos. Construido con Django 5.x, Django REST Framework y PostgreSQL 13+.

**✅ Proyecto cumpliendo criterios Senior** según Prueba Técnica Unificada Django - DARIENT TECHNOLOGY

## 📋 Tabla de Contenidos

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Docker](#docker)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Decisiones Técnicas](#decisiones-técnicas)
- [Nivel de Cumplimiento](#nivel-de-cumplimiento)

## 🚀 Características

### Funcionalidades Principales
- ✅ CRUD completo para Bancos, Clientes y Créditos
- ✅ Autenticación JWT (token + refresh)
- ✅ Validaciones a nivel de modelo, serializer y base de datos
- ✅ Filtrado, búsqueda y ordenamiento avanzado
- ✅ Paginación automática
- ✅ Documentación API interactiva (Swagger/ReDoc)
- ✅ Health check endpoint
- ✅ Envío de emails al crear créditos
- ✅ Logging estructurado
- ✅ Tests con pytest
- ✅ **Arquitectura escalable con Service Layer** (Patrón Senior)
- ✅ **Type hints** para mejor documentación y detección de errores

### Validaciones Implementadas
- **Cliente**: Edad coherente con fecha de nacimiento, email único, campos obligatorios
- **Crédito**: `pago_minimo <= pago_maximo`, validación de relaciones
- **Banco**: Nombre único, tipo válido
- Prevención de eliminación de registros con relaciones activas

## 🏗️ Arquitectura

### Principios de Diseño
- **API-First**: Todo el CRUD y operación diaria se realiza exclusivamente vía API REST
- **Django Admin**: Habilitado técnicamente pero fuera del scope del producto (herramienta interna)
- **Separación de responsabilidades**: Arquitectura en capas (Models, Serializers, Services, Views)
- **Service Layer Pattern**: Lógica de negocio separada en servicios reutilizables
- **Sin lógica duplicada**: Validaciones centralizadas y reutilizables
- **Type Safety**: Type hints para mejor mantenibilidad y detección temprana de errores

### Arquitectura en Capas

El proyecto implementa una **arquitectura en capas** siguiendo buenas prácticas de desarrollo Senior:

```
┌─────────────────────────────────────────┐
│          Capa de Presentación           │
│  (ViewSets - Endpoints API REST)        │
│  - Coordinación de requests/responses   │
│  - Validación de permisos               │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│        Capa de Lógica de Negocio        │
│  (Services - Business Logic)            │
│  - Validaciones de negocio              │
│  - Operaciones complejas                │
│  - Transacciones de base de datos       │
│  - Reutilizable y testeable             │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Capa de Serialización           │
│  (Serializers - Data Transformation)    │
│  - Validación de entrada                │
│  - Transformación de datos              │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│          Capa de Datos                  │
│  (Models - Database Layer)              │
│  - Definición de entidades              │
│  - Relaciones y constraints             │
│  - Validaciones a nivel DB              │
└─────────────────────────────────────────┘
```

**Ejemplo de flujo con Service Layer:**
```python
# View (Capa de Presentación)
class ClienteViewSet(viewsets.ModelViewSet):
    def destroy(self, request, *args, **kwargs):
        cliente = self.get_object()
        # Delega lógica de negocio al servicio
        result = ClienteService.delete_cliente_if_safe(cliente)
        if not result['success']:
            return Response(result, status=400)
        return Response(status=204)

# Service (Capa de Lógica de Negocio)
class ClienteService:
    @staticmethod
    def delete_cliente_if_safe(cliente: Cliente) -> Dict[str, Any]:
        # Valida reglas de negocio
        if cliente.creditos.exists():
            return {
                'success': False,
                'error': 'No se puede eliminar cliente con créditos'
            }
        # Ejecuta operación
        with transaction.atomic():
            cliente.delete()
        return {'success': True}
```

### Stack Tecnológico

#### Backend
- **Python 3.12** (recomendado) o Python 3.11+
- **Django 5.0.4**
- **Django REST Framework 3.15.1**
- **PostgreSQL 13+**

#### Autenticación y Seguridad
- **djangorestframework-simplejwt**: Autenticación JWT
- **CSP (Content Security Policy)**: Headers de seguridad
- **Permissions-Policy**: Control de permisos

#### Documentación
- **drf-spectacular**: Generación automática de esquemas OpenAPI/Swagger

#### Desarrollo
- **pytest + pytest-django**: Framework de testing
- **django-filter**: Filtrado avanzado
- **django-environ**: Gestión de variables de entorno
- **python-dateutil**: Manejo de fechas y cálculos de edad

#### Infraestructura
- **Docker + Docker Compose**: Contenedorización con multi-stage build optimizado
- **psycopg2-binary**: Driver PostgreSQL
- **python-json-logger**: Logging estructurado en formato JSON

## 📦 Requisitos

- Python 3.12 (recomendado) o Python 3.11+
- PostgreSQL 13 o superior
- Docker y Docker Compose (opcional, para desarrollo con contenedores)
- pip (gestor de paquetes Python)

## 🔧 Instalación

### Opción 1: Desarrollo Local (Recomendado para desarrollo)

1. **Clonar el repositorio**
```bash
cd "C:\Users\dylan\Desktop\Tu Credito"
```

2. **Crear entorno virtual**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Copiar archivo de ejemplo
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows

# Editar .env con tus valores según tus necesidades
```

5. **Configurar base de datos**
```bash
# Crear base de datos PostgreSQL
createdb tu_credito_db
# O usando psql
psql -U postgres -c "CREATE DATABASE tu_credito_db;"
```

6. **Inicializar base de datos (Primera vez)**

**Windows:**
```bash
cd back
scripts\init_db.bat
```

**Linux/Mac:**
```bash
cd back
chmod +x scripts/init_db.sh
./scripts/init_db.sh
```

Este script ejecuta todas las migraciones y crea un superusuario inicial.

**O manualmente:**
```bash
# Activar entorno virtual primero
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

python manage.py migrate
python manage.py createsuperuser
```

7. **Actualizar base de datos (Cuando hay cambios en modelos)**

Cada vez que se agreguen o modifiquen modelos, ejecuta las migraciones:

**Windows:**
```bash
cd back
scripts\migrate.bat
```

**Linux/Mac:**
```bash
cd back
chmod +x scripts/migrate.sh
./scripts/migrate.sh
```

**O manualmente:**
```bash
# Activar entorno virtual primero
python manage.py migrate
```

**Para migrar una app específica:**
```bash
# Windows
scripts\migrate.bat creditos

# Linux/Mac
./scripts/migrate.sh creditos

# O manualmente
python manage.py migrate creditos
```

**Nota importante sobre datos existentes:**
- ✅ Los datos existentes **NO se pierden** al ejecutar migraciones
- ✅ Solo se agregan/modifican columnas según los cambios en los modelos
- ✅ Los campos nuevos con `default` se llenan automáticamente
- ✅ Los campos `null=True` quedan en NULL hasta que se calculen/actualicen

8. **Crear superusuario (opcional, solo para Django Admin interno)**
```bash
python manage.py createsuperuser
```

9. **Ejecutar servidor de desarrollo**

**Windows:**
```bash
cd back
# Activar entorno virtual
venv\Scripts\activate
python manage.py runserver
```

**Linux/Mac:**
```bash
cd back
# Activar entorno virtual
source venv/bin/activate
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

### Opción 2: Docker Compose (Recomendado para producción/dev)

1. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env según necesidades
```

2. **Construir y ejecutar contenedores**
```bash
docker-compose up --build
```

Los servicios estarán disponibles en:
- **Backend**: `http://localhost:8000`
- **PostgreSQL**: `localhost:5432`

## ⚙️ Configuración

### Variables de Entorno

El proyecto incluye un archivo `.env.example` como template. Para configurar:

1. **Copiar el archivo de ejemplo:**
```bash
# Linux/Mac
cp .env.example .env

# Windows
copy .env.example .env
```

2. **Editar `.env` con tus valores:**

```env
# Django
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database - PostgreSQL
# NOTA: En la URL, los caracteres especiales deben estar codificados: @ = %40, # = %23, ! = %21
DATABASE_URL=postgresql://postgres:password@localhost:5432/tu_credito_db

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-here

# Email (Console backend para desarrollo, SMTP para producción)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Logging
LOG_LEVEL=INFO
```

**Importante:** El archivo `.env` está en `.gitignore` y no debe subirse al repositorio.

### Settings por Entorno

El proyecto utiliza configuración separada por entorno:
- **`tu_credito/settings/base.py`**: Configuración base común
- **`tu_credito/settings/dev.py`**: Configuración de desarrollo
- **`tu_credito/settings/prod.py`**: Configuración de producción

Cambiar el settings en `manage.py` según el entorno:
```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_credito.settings.dev')  # o 'prod'
```

## 📖 Uso

### Autenticación JWT

1. **Obtener tokens de acceso**
```bash
POST /api/auth/token/
Content-Type: application/json

{
    "username": "tu_usuario",
    "password": "tu_contraseña"
}

Response:
{
    "access": "token_de_acceso",
    "refresh": "token_de_refresh"
}
```

2. **Usar token en requests**
```bash
GET /api/bancos/
Authorization: Bearer <token_de_acceso>
```

3. **Refrescar token**
```bash
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "token_de_refresh"
}
```

### Endpoints Disponibles

#### Bancos
- `GET /api/bancos/` - Listar bancos (filtros: nombre, tipo)
- `POST /api/bancos/` - Crear banco
- `GET /api/bancos/{id}/` - Obtener banco
- `PUT /api/bancos/{id}/` - Actualizar banco completo
- `PATCH /api/bancos/{id}/` - Actualizar banco parcial
- `DELETE /api/bancos/{id}/` - Eliminar banco

#### Clientes
- `GET /api/clientes/` - Listar clientes (filtros: nombre, email, tipo_persona, edad, banco)
- `POST /api/clientes/` - Crear cliente (edad calculada automáticamente)
- `GET /api/clientes/{id}/` - Obtener cliente
- `PUT /api/clientes/{id}/` - Actualizar cliente completo
- `PATCH /api/clientes/{id}/` - Actualizar cliente parcial
- `DELETE /api/clientes/{id}/` - Eliminar cliente (solo si no tiene créditos)

#### Créditos
- `GET /api/creditos/` - Listar créditos (múltiples filtros disponibles)
- `POST /api/creditos/` - Crear crédito (envía email automático)
- `GET /api/creditos/{id}/` - Obtener crédito
- `PUT /api/creditos/{id}/` - Actualizar crédito completo
- `PATCH /api/creditos/{id}/` - Actualizar crédito parcial
- `DELETE /api/creditos/{id}/` - Eliminar crédito

#### Health Check
- `GET /health/` - Verificar estado del sistema (no requiere autenticación)

### Ejemplos de Uso

#### Crear un Banco
```bash
POST /api/bancos/
Authorization: Bearer <token>
Content-Type: application/json

{
    "nombre": "Banco Popular",
    "tipo": "PRIVADO",
    "direccion": "Calle 50 # 12-34"
}
```

#### Crear un Cliente
```bash
POST /api/clientes/
Authorization: Bearer <token>
Content-Type: application/json

{
    "nombre_completo": "Juan Pérez",
    "fecha_nacimiento": "1990-05-15",
    "email": "juan.perez@example.com",
    "telefono": "+57 300 123 4567",
    "tipo_persona": "NATURAL",
    "nacionalidad": "Colombiana"
}
```

#### Crear un Crédito
```bash
POST /api/creditos/
Authorization: Bearer <token>
Content-Type: application/json

{
    "cliente": 1,
    "banco": 1,
    "descripcion": "Crédito comercial para ampliación de negocio",
    "pago_minimo": "1000.00",
    "pago_maximo": "5000.00",
    "plazo_meses": 24,
    "tipo_credito": "COMERCIAL"
}
```

#### Filtrar y Buscar
```bash
# Filtrar clientes por edad
GET /api/clientes/?edad_min=25&edad_max=40

# Buscar créditos por descripción
GET /api/creditos/?search=comercial

# Ordenar bancos por nombre
GET /api/bancos/?ordering=nombre
```

## 📚 API Documentation

### Swagger UI (Interactivo)
```
http://localhost:8000/api/docs/
```

### ReDoc (Alternativa)
```
http://localhost:8000/api/redoc/
```

### Esquema OpenAPI (JSON)
```
http://localhost:8000/api/schema/
```

La documentación incluye:
- Descripción de todos los endpoints
- Esquemas de request/response
- Ejemplos de uso
- Autenticación JWT integrada
- Tags organizados por dominio

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=apps --cov-report=html

# Tests específicos
pytest tests/test_bancos.py
pytest tests/test_clientes.py
pytest tests/test_creditos.py

# Tests con verbosidad
pytest -v
```

### Estructura de Tests

Los tests cubren:
- ✅ Validaciones de modelos
- ✅ Endpoints CRUD completos
- ✅ Filtros y búsquedas
- ✅ Autenticación y permisos
- ✅ Validaciones de negocio (edad, pagos, etc.)
- ✅ Health check endpoint

### Fixtures Disponibles

- `api_client`: Cliente API sin autenticación
- `authenticated_client`: Cliente API con JWT token
- `banco`: Fixture para crear banco en tests
- `cliente`: Fixture para crear cliente en tests

## 🐳 Docker

### Características del Dockerfile
- **Multi-stage build**: Optimización de tamaño de imagen
- **Health check**: Verificación automática del estado del servicio
- **Producción-ready**: Configurado para despliegue en cloud

### Desarrollo con Docker

```bash
# Construir y levantar servicios
docker-compose up --build

# En background
docker-compose up -d

# Ver logs
docker-compose logs -f backend

# Ejecutar migraciones (primera vez o actualizaciones)
docker-compose exec backend python manage.py migrate

# Ejecutar tests
docker-compose exec backend pytest

# Ejecutar tests con cobertura
docker-compose exec backend pytest --cov=apps --cov-report=html

# Crear superusuario
docker-compose exec backend python manage.py createsuperuser

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

### Servicios en docker-compose.yml
- **backend**: Django API con health checks
- **db**: PostgreSQL 13 con persistencia de datos

## 📁 Estructura del Proyecto

```
tu_credito/
├── apps/
│   ├── bancos/           # App de Bancos
│   │   ├── models.py     # Capa de datos
│   │   ├── serializers.py # Capa de serialización
│   │   ├── views.py      # Capa de presentación (ViewSets)
│   │   ├── services.py   # Capa de lógica de negocio ✨
│   │   ├── filters.py    # Capa de consultas/filtros
│   │   ├── urls.py       # Rutas de la app
│   │   └── migrations/   # Migraciones de base de datos
│   ├── clientes/         # App de Clientes
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── services.py   # Capa de lógica de negocio ✨
│   │   ├── filters.py
│   │   ├── urls.py
│   │   └── migrations/
│   ├── creditos/         # App de Créditos
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── services.py   # Capa de lógica de negocio ✨
│   │   ├── filters.py
│   │   ├── signals.py    # Envío de emails
│   │   ├── urls.py
│   │   └── migrations/
│   └── core/             # App core (utils, health)
│       ├── views.py      # Health check
│       ├── exceptions.py # Exception handler personalizado
│       └── urls.py       # URLs centrales (auth, health)
├── tu_credito/
│   ├── settings/
│   │   ├── base.py       # Settings base (común)
│   │   ├── dev.py        # Settings desarrollo
│   │   └── prod.py       # Settings producción
│   ├── urls.py           # URLs principales del proyecto
│   ├── wsgi.py
│   └── asgi.py
├── tests/                # Tests automatizados
│   ├── test_bancos.py
│   ├── test_clientes.py
│   ├── test_creditos.py
│   └── test_health.py
├── conftest.py           # Fixtures compartidos de pytest
├── pytest.ini            # Configuración pytest
├── manage.py
├── requirements.txt
├── Dockerfile            # Multi-stage build optimizado
├── docker-compose.yml    # Orquestación de servicios
├── .env.example          # Template de variables de entorno
└── README.md

✨ = Arquitectura Senior: Service Layer Pattern
```

## 🎯 Decisiones Técnicas

### Arquitectura y Patrones de Diseño
- **Service Layer Pattern**: Separación de lógica de negocio de las vistas
  - `ClienteService`, `BancoService`, `CreditoService`
  - Lógica reutilizable y testeable independientemente
  - Facilita mantenimiento y escalabilidad
- **Repository Pattern**: Modelos Django actúan como repositorios de datos
- **ViewSet Pattern**: CRUD estándar con DRF para consistencia
- **Signal Pattern**: Events desacoplados (envío de emails)

### Modelos y Validaciones
- **Validaciones en múltiples capas**: Modelo (`clean()`), Serializer y Base de datos (constraints)
- **Cálculo automático de edad**: Se calcula en el modelo basándose en `fecha_nacimiento`
- **Índices en campos frecuentemente consultados**: email, tipo_persona, fecha_registro, etc.
- **Prevención de eliminación en cascada**: Validaciones antes de eliminar registros con relaciones (implementado en Services)

### API REST
- **ViewSets en lugar de Views**: Código más limpio y mantenible
- **Serializers separados para list/detail**: Optimización de queries (select_related, prefetch_related)
- **Filtrado con django-filter**: Filtros consistentes y reutilizables
- **Paginación estándar**: 20 elementos por página (configurable)
- **Lógica de negocio en Services**: Las vistas delegan la lógica de negocio a los servicios

### Autenticación
- **JWT tokens**: Stateless, escalable, adecuado para APIs
- **Refresh tokens**: Rotación automática de tokens
- **Permisos por defecto IsAuthenticated**: Todas las operaciones requieren autenticación (excepto health check)

### Seguridad
- **CSP headers**: Content Security Policy configurado
- **XSS protection**: Headers de seguridad habilitados
- **Validación de entrada**: En serializers y modelos
- **Variables de entorno**: Secretos no hardcodeados

### Testing
- **pytest + pytest-django**: Framework moderno y flexible
- **Fixtures reutilizables**: Cliente API, usuarios, modelos de prueba
- **Tests de validaciones críticas**: Edad, pagos, relaciones
- **Tests de lógica de negocio**: Servicios testeados independientemente
- **Cobertura**: Tests para endpoints principales, modelos y servicios
- **Coverage configurado**: `pytest --cov` para medir cobertura de código

### Logging
- **Logging estructurado**: Formato JSON para producción
- **Niveles configurables**: Por entorno
- **Contexto adicional**: IDs, información relevante

### Email
- **Signals de Django**: Desacoplado de la lógica de negocio
- **Console backend en desarrollo**: Emails en consola
- **Configurable**: Fácil cambiar a SMTP en producción

### Calidad de Código
- **Type hints**: Funciones críticas con tipos explícitos para mejor IDE support y documentación
- **Docstrings completos**: Documentación inline en clases y métodos importantes
- **Exception handling**: Handler personalizado para respuestas de error consistentes
- **Logging estructurado**: Formato JSON para mejor análisis en producción

## 🔒 Seguridad

- Todas las rutas API requieren autenticación JWT (excepto `/health/`)
- Variables de entorno para secretos
- Validación de entrada en múltiples capas
- Headers de seguridad configurados (CSP, XSS Protection)
- Validación de relaciones antes de eliminar registros

## 🚀 Próximos Pasos / Mejoras Futuras

- [ ] Cache con Redis
- [ ] Rate limiting
- [ ] Internacionalización (i18n)
- [ ] Webhooks para eventos
- [ ] Exportación de reportes (PDF, Excel)
- [ ] Integración con servicios de terceros
- [ ] Auditoría de cambios (django-auditlog)
- [ ] GraphQL API (opcional)

## 🏆 Nivel de Cumplimiento

Este proyecto cumple con los **Criterios de Evaluación por Nivel = Senior** según la Prueba Técnica Unificada Django de DARIENT TECHNOLOGY.

### ✅ Cumplimiento Senior

- ✅ **Arquitectura clara y escalable**: Service Layer Pattern implementado
- ✅ **Uso de patrones**: Service Layer, Repository, ViewSet, Signal
- ✅ **Pruebas automatizadas**: pytest + pytest-django con cobertura
- ✅ **Contenedores Docker**: Multi-stage build optimizado para producción
- ✅ **Configuración profesional**: Settings por entorno, variables de entorno
- ✅ **Seguridad sólida**: CSP, JWT, validaciones múltiples, exception handling
- ✅ **Type hints**: Documentación implícita y mejor IDE support
- ✅ **Logging estructurado**: Formato JSON para análisis en producción

Para más detalles, ver [`EVALUACION_SENIOR.md`](EVALUACION_SENIOR.md).

## 📝 Notas Importantes

### Django Admin
- Django Admin está **habilitado técnicamente** pero **NO forma parte del producto**
- Es una herramienta interna solo para desarrollo/debugging
- No debe documentarse ni presentarse como parte de la solución
- El CRUD y operación diaria se realiza exclusivamente vía API REST

### Migraciones

**Ubicación:** Las migraciones están en cada app bajo `apps/*/migrations/`

**Inicialización (primera vez):**

**Windows:**
```bash
cd back
scripts\init_db.bat
```

**Linux/Mac:**
```bash
cd back
chmod +x scripts/init_db.sh
./scripts/init_db.sh
```

**Actualización (cuando hay cambios en modelos):**

**Windows:**
```bash
cd back
scripts\migrate.bat
```

**Linux/Mac:**
```bash
cd back
chmod +x scripts/migrate.sh
./scripts/migrate.sh
```

**Comandos útiles:**
```bash
# Ver estado de migraciones
python manage.py showmigrations

# Crear nueva migración después de modificar modelos
python manage.py makemigrations

# Aplicar todas las migraciones
python manage.py migrate

# Aplicar migraciones de una app específica
python manage.py migrate creditos
```

**Importante sobre datos existentes:**
- ✅ Los datos existentes **NO se pierden** al ejecutar migraciones
- ✅ Solo se agregan/modifican columnas según los cambios en los modelos
- ✅ Los campos nuevos con `default` se llenan automáticamente
- ✅ Los campos `null=True` quedan en NULL hasta que se calculen/actualicen
- ⚠️ Siempre haz backup antes de migraciones en producción

### Service Layer
- La lógica de negocio está separada en archivos `services.py` dentro de cada app
- Las vistas delegan operaciones complejas a los servicios
- Esto facilita el testing unitario y mantiene el código modular y escalable

### Uso de IA (si aplica)

Si utilizaste herramientas de IA (ChatGPT, Copilot, Cursor, Claude, etc.) durante el desarrollo:

**Por favor documenta:**
1. En qué parte del proceso la utilizaste
2. Por qué te pareció apropiado usarla en ese caso

**Ejemplo:**
- **Inicio de proyecto**: Usé IA para generar la estructura inicial de archivos siguiendo las convenciones de Django
- **Documentación**: Usé IA para generar plantillas de docstrings consistentes
- **Debugging**: Usé IA para identificar problemas en queries de base de datos

_Nota: Si no utilizaste IA, indica "No se utilizó IA en el desarrollo de este proyecto"._

## 👥 Contribución

1. Crear rama para feature: `git checkout -b feature/nueva-funcionalidad`
2. Hacer commits descriptivos
3. Ejecutar tests: `pytest`
4. Crear Pull Request

## 📄 Licencia

Este proyecto es parte de una prueba técnica.

---

**Desarrollado con ❤️ usando Django y Django REST Framework**
# tu-credito-back
