from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from entities.base import Base

class Producto(Base):
    __tablename__ = 'Productos'

    producto_id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String)
    precio = Column(Float, nullable=False)
    costo = Column(Float, nullable=False)

    marca_id = Column(Integer, ForeignKey('Marcas.marca_id'), nullable=False)  # 👈 clave foránea correcta
    categoria_id = Column(Integer, ForeignKey('Categorias.categoria_id'), nullable=False)

    genero = Column(Enum('Hombre', 'Mujer', 'Unisex', 'Niño', 'Niña'), nullable=False)
    temporada = Column(Enum('Verano', 'Invierno', 'Primavera', 'Otoño', 'All Season'), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.utcnow)
    estado = Column(Enum('Activo', 'Inactivo'), default='Activo')

    marca = relationship("Marca", back_populates="productos")      
    categoria = relationship("Categoria", back_populates="productos")
    detalles = relationship("DetalleVenta", back_populates="producto")
    detalles_compra = relationship("DetalleCompra", back_populates="producto")
    inventarios = relationship("Inventario", back_populates="producto")