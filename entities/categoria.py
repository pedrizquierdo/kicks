from sqlalchemy import Column, Integer, String, Enum, Text
from sqlalchemy.orm import relationship
from entities.base import Base

class Categoria(Base):
    __tablename__ = 'Categorias'
    
    categoria_id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(Text)
    tipo = Column(Enum('Calzado', 'Ropa', 'Accesorios', name='tipo_categoria'), nullable=False)
    
    productos = relationship("Producto", back_populates="categoria")