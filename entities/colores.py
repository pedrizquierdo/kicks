from sqlalchemy import Column, Integer, String
from entities.base import Base


class Color(Base):
    __tablename__ = 'colores'
    color_id = Column(Integer, primary_key=True)
    nombre = Column(String(30), nullable=False)
    codigo_hex = Column(String(7))