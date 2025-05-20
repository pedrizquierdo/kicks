from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from entities.base import Base

class Proveedor(Base):
    __tablename__ = 'Proveedores'

    proveedor_id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    contacto = Column(String(100))
    telefono = Column(String(20))
    email = Column(String(100))
    direccion = Column(String)
    tipo_producto = Column(Enum('Calzado', 'Ropa', 'Ambos'), nullable=False)

    compras = relationship("Compra", back_populates="proveedor")  
