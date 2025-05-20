
from datetime import datetime, timezone
from sqlalchemy import DECIMAL, CheckConstraint, Column, Date, DateTime, Enum, ForeignKey, Integer, String, Text
from entities.base import Base
class Resena(Base):
    __tablename__ = 'resenas'
    resena_id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey('productos.producto_id'))
    cliente_id = Column(Integer, ForeignKey('clientes.cliente_id'))
    calificacion = Column(Integer, nullable=False)
    comentario = Column(Text)
    fecha = Column(DateTime, default=datetime.now(timezone.utc))

    __table_args__ = (
        CheckConstraint('calificacion BETWEEN 1 AND 5', name='check_calificacion_range'),
    )
