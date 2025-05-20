from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from entities.base import Base

class DetalleCompra(Base):
    __tablename__ = 'Detalle_Compras'

    detalle_id = Column(Integer, primary_key=True)
    compra_id = Column(Integer, ForeignKey('Compras.compra_id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('Productos.producto_id'), nullable=False)  # ✅ CLAVE FORÁNEA

    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    compra = relationship("Compra", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_compra")
    compra_id = Column(Integer, ForeignKey('Compras.compra_id'), nullable=False)
    