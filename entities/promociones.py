from sqlalchemy import DECIMAL, Column, Date, Enum, ForeignKey, Integer, String, Text
from entities.base import Base


class Promocion(Base):
    __tablename__ = 'promociones'
    promocion_id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    descuento_porcentaje = Column(DECIMAL(5, 2), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    productos_aplicables = Column(Enum('Todos', 'Categoría específica', 'Marca específica'), nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.categoria_id'))
    marca_id = Column(Integer, ForeignKey('marcas.marca_id'))