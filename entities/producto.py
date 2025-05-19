from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from entities.base import Base

class Producto(Base):
    __tablename__ = 'Productos'
    
    producto_id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    precio = Column(Numeric(10, 2), nullable=False)
    costo = Column(Numeric(10, 2), nullable=False)
    marca_id = Column(Integer, ForeignKey('Marcas.marca_id'), nullable=False)
    categoria_id = Column(Integer, ForeignKey('Categorias.categoria_id'), nullable=False)
    genero = Column(Enum('Hombre', 'Mujer', 'Unisex', 'Niño', 'Niña', name='genero_producto'), nullable=False)
    temporada = Column(Enum('Verano', 'Invierno', 'Primavera', 'Otoño', 'All Season', name='temporada_producto'), nullable=False)
    fecha_creacion = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    fecha_actualizacion = Column(DateTime, onupdate='CURRENT_TIMESTAMP')
    estado = Column(Enum('Activo', 'Inactivo', name='estado_producto'), default='Activo')
    
    marca = relationship("Marca", back_populates="productos")
    categoria = relationship("Categoria", back_populates="productos")
    inventarios = relationship("Inventario", back_populates="producto")
    