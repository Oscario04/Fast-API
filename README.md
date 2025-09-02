# Sistema de Monitoreo de Inundaciones

Sistema API para el monitoreo y reporte de inundaciones con capacidades GIS usando FastAPI, PostgreSQL y PostGIS.

## Estructura de la Base de Datos

### Tablas principales:

1. **estaciones** - Estaciones pluviométricas con ubicación geográfica
2. **reportes_inundacion** - Reportes de inundaciones con relación a estaciones
3. **red_vial** - Red vial con geometrías de líneas
4. **zonas_riesgo** - Zonas de riesgo con polígonos

## Requisitos

- Python 3.8+
- PostgreSQL 12+
- PostGIS 3+

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar base de datos PostgreSQL:
```bash
# Crear base de datos
createdb inundaciones

# Habilitar PostGIS
psql -d inundaciones -c "CREATE EXTENSION postgis;"
```

3. Configurar variables de entorno en `.env`:
```env
DATABASE_URL=postgresql+asyncpg://usuario:password@localhost:5432/inundaciones
SYNC_DATABASE_URL=postgresql://usuario:password@localhost:5432/inundaciones
```

4. Inicializar la base de datos:
```bash
python scripts/init_db.py
```

## Uso

1. Ejecutar la aplicación:
```bash
uvicorn main:app --reload
```

2. Acceder a la documentación de la API:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints disponibles

- `GET /` - Página principal
- `GET /estaciones` - Listar todas las estaciones
- `GET /estaciones/{id}` - Obtener estación específica
- `GET /reportes` - Listar todos los reportes
- `POST /reportes` - Crear nuevo reporte
- `GET /red-vial` - Listar red vial
- `GET /zonas-riesgo` - Listar zonas de riesgo
- `GET /estadisticas` - Obtener estadísticas del sistema

## Características GIS

- Consultas espaciales con PostGIS
- Geometrías en formato GeoJSON
- Soporte para puntos, líneas y polígonos
- Consultas de intersección y distancia

## Migraciones

Para crear migraciones con Alembic:

```bash
# Crear nueva migración
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head
```

## Desarrollo

La estructura del proyecto sigue las mejores prácticas para FastAPI:
- Separación de modelos, rutas y configuración de base de datos
- Soporte para operaciones asíncronas
- Validación automática de datos
- Documentación automática de API
