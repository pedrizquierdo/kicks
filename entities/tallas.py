from sqlalchemy import DECIMAL, Column, Date, Enum, ForeignKey, Integer, String, Text
from entities.base import Base
class Talla(Base):
    __tablename__ = 'tallas'
    talla_id = Column(Integer, primary_key=True)
    tipo = Column(Enum('Calzado', 'Ropa'), nullable=False)
    valor = Column(String(10), nullable=False)
    descripcion = Column(String(50))