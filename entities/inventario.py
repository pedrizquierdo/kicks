from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from entities.base import Base

class Inventario(Base):
    __tablename__ = 'Inventario'
    
    inventario_id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey('Productos.producto_id'), nullable=False)
    talla = Column(String(10), nullable=False)
    color = Column(String(30), nullable=False)
    cantidad_disponible = Column(Integer, nullable=False, default=0)
    ubicacion_almacen = Column(String(50))
    fecha_ultima_entrada = Column(DateTime)
    fecha_ultima_salida = Column(DateTime)
    
    producto = relationship("Producto", back_populates="inventarios")
    