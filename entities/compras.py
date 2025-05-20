from sqlalchemy import Column, Integer, Float, Enum, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from entities.base import Base

class Compra(Base):
    __tablename__ = 'Compras'

    compra_id = Column(Integer, primary_key=True)
    proveedor_id = Column(Integer, ForeignKey('Proveedores.proveedor_id'), nullable=False)
    fecha_pedido = Column(DateTime, default=datetime.utcnow)
    fecha_entrega_esperada = Column(Date)
    fecha_entrega_real = Column(Date)
    total = Column(Float, nullable=False)
    estado = Column(Enum('Pendiente', 'Recibido', 'Cancelado'), default='Pendiente')

    proveedor_id = Column(Integer, ForeignKey('Proveedores.proveedor_id'), nullable=False)
    proveedor = relationship("Proveedor", back_populates="compras")
    detalles = relationship("DetalleCompra", back_populates="compra")
