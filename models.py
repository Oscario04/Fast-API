from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from geoalchemy2 import Geometry
from database import Base

class Estacion(Base):
    __tablename__ = "estaciones"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String)
    geom = Column(Geometry("POINT", srid=4326))

class ReporteInundacion(Base):
    __tablename__ = "reportes_inundacion"
    
    id = Column(Integer, primary_key=True, index=True)
    estacion_id = Column(Integer, ForeignKey("estaciones.id"))
    fecha = Column(DateTime, nullable=False)
    descripcion = Column(String)
    nivel_agua = Column(Float)
    geom = Column(Geometry("POINT", srid=4326))

class RedVial(Base):
    __tablename__ = "red_vial"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    tipo = Column(String)
    geom = Column(Geometry("LINESTRING", srid=4326))

class ZonaRiesgo(Base):
    __tablename__ = "zonas_riesgo"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    categoria = Column(String)
    geom = Column(Geometry("POLYGON", srid=4326))
