from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from geoalchemy2.functions import ST_AsGeoJSON, ST_Intersects, ST_Distance
import json

from database import get_session
from models import Estacion, ReporteInundacion, RedVial, ZonaRiesgo

app = FastAPI(
    title="Sistema de Monitoreo de Inundaciones",
    description="API para el monitoreo y reporte de inundaciones con capacidades GIS",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Sistema de Monitoreo de Inundaciones API"}

@app.get("/estaciones")
async def listar_estaciones(session: AsyncSession = Depends(get_session)):
    """Lista todas las estaciones pluviométricas"""
    result = await session.execute(select(Estacion))
    estaciones = result.scalars().all()
    return {
        "estaciones": [
            {
                "id": e.id,
                "nombre": e.nombre,
                "tipo": e.tipo,
                "geom": json.loads((await session.execute(ST_AsGeoJSON(e.geom))).scalar())
            } for e in estaciones
        ]
    }

@app.get("/estaciones/{estacion_id}")
async def obtener_estacion(estacion_id: int, session: AsyncSession = Depends(get_session)):
    """Obtiene una estación específica por ID"""
    result = await session.execute(
        select(Estacion).where(Estacion.id == estacion_id)
    )
    estacion = result.scalar_one_or_none()
    
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no encontrada")
    
    return {
        "id": estacion.id,
        "nombre": estacion.nombre,
        "tipo": estacion.tipo,
        "geom": json.loads((await session.execute(ST_AsGeoJSON(estacion.geom))).scalar())
    }

@app.get("/reportes")
async def listar_reportes(session: AsyncSession = Depends(get_session)):
    """Lista todos los reportes de inundación"""
    result = await session.execute(
        select(ReporteInundacion, Estacion.nombre)
        .join(Estacion, ReporteInundacion.estacion_id == Estacion.id)
    )
    reportes = result.all()
    
    return {
        "reportes": [
            {
                "id": reporte.id,
                "estacion_id": reporte.estacion_id,
                "estacion_nombre": nombre,
                "fecha": reporte.fecha.isoformat(),
                "descripcion": reporte.descripcion,
                "nivel_agua": reporte.nivel_agua,
                "geom": json.loads((await session.execute(ST_AsGeoJSON(reporte.geom))).scalar())
            } for reporte, nombre in reportes
        ]
    }

@app.post("/reportes")
async def crear_reporte(
    estacion_id: int,
    descripcion: str,
    nivel_agua: float = None,
    session: AsyncSession = Depends(get_session)
):
    """Crea un nuevo reporte de inundación"""
    # Verificar que la estación existe
    result = await session.execute(
        select(Estacion).where(Estacion.id == estacion_id)
    )
    estacion = result.scalar_one_or_none()
    
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no encontrada")
    
    # Crear el reporte usando la geometría de la estación
    nuevo_reporte = ReporteInundacion(
        estacion_id=estacion_id,
        fecha=func.now(),
        descripcion=descripcion,
        nivel_agua=nivel_agua,
        geom=estacion.geom  # Usar la misma geometría que la estación
    )
    
    session.add(nuevo_reporte)
    await session.commit()
    await session.refresh(nuevo_reporte)
    
    return {
        "message": "Reporte creado exitosamente",
        "reporte_id": nuevo_reporte.id
    }

@app.get("/red-vial")
async def listar_red_vial(session: AsyncSession = Depends(get_session)):
    """Lista toda la red vial"""
    result = await session.execute(select(RedVial))
    vias = result.scalars().all()
    
    return {
        "red_vial": [
            {
                "id": v.id,
                "nombre": v.nombre,
                "tipo": v.tipo,
                "geom": json.loads((await session.execute(ST_AsGeoJSON(v.geom))).scalar())
            } for v in vias
        ]
    }

@app.get("/zonas-riesgo")
async def listar_zonas_riesgo(session: AsyncSession = Depends(get_session)):
    """Lista todas las zonas de riesgo"""
    result = await session.execute(select(ZonaRiesgo))
    zonas = result.scalars().all()
    
    return {
        "zonas_riesgo": [
            {
                "id": z.id,
                "nombre": z.nombre,
                "categoria": z.categoria,
                "geom": json.loads((await session.execute(ST_AsGeoJSON(z.geom))).scalar())
            } for z in zonas
        ]
    }

@app.get("/estadisticas")
async def obtener_estadisticas(session: AsyncSession = Depends(get_session)):
    """Obtiene estadísticas del sistema"""
    # Contar estaciones
    result = await session.execute(select(func.count(Estacion.id)))
    total_estaciones = result.scalar()
    
    # Contar reportes
    result = await session.execute(select(func.count(ReporteInundacion.id)))
    total_reportes = result.scalar()
    
    # Último reporte
    result = await session.execute(
        select(ReporteInundacion)
        .order_by(ReporteInundacion.fecha.desc())
        .limit(1)
    )
    ultimo_reporte = result.scalar_one_or_none()
    
    return {
        "total_estaciones": total_estaciones,
        "total_reportes": total_reportes,
        "ultimo_reporte": ultimo_reporte.fecha.isoformat() if ultimo_reporte else None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
