from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from entities.base import Base

class DetalleVenta(Base):
    __tablename__ = 'Detalle_Ventas'

    detalle_id = Column(Integer, primary_key=True)
    venta_id = Column(Integer, ForeignKey('Ventas.venta_id'), nullable=False)  
    producto_id = Column(Integer, ForeignKey('Productos.producto_id'), nullable=False)

    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    descuento = Column(Float, default=0)
    subtotal = Column(Float, nullable=False)

    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles")