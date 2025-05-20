from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from entities.base import Base

class Marca(Base):
    __tablename__ = 'Marcas'

    marca_id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String)
    pais_origen = Column(String(50))
    sitio_web = Column(String(100))

    productos = relationship("Producto", back_populates="marca")  