from sqlalchemy import Column, Integer, Float, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from entities.base import Base

class Venta(Base):
    __tablename__ = 'Ventas'

    venta_id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('Clientes.cliente_id'))
    empleado_id = Column(Integer, ForeignKey('Empleados.empleado_id'))
    fecha_venta = Column(DateTime, default=datetime.utcnow)
    total = Column(Float, nullable=False)
    metodo_pago = Column(Enum('Efectivo', 'Tarjeta', 'Transferencia'), nullable=False)
    estado = Column(Enum('Completada', 'Cancelada', 'En proceso'), default='Completada')

    detalles = relationship("DetalleVenta", back_populates="venta")  
    cliente = relationship("Cliente", back_populates="ventas")
    empleado = relationship("Empleado", back_populates="ventas")
    empleado_id = Column(Integer, ForeignKey('Empleados.empleado_id'))  # ✅ CLAVE FORÁNEA
    empleado = relationship("Empleado", back_populates="ventas") 
