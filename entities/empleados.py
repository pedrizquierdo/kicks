from sqlalchemy import Column, Integer, String, Enum, Float, Date
from sqlalchemy.orm import relationship
from entities.base import Base

class Empleado(Base):
    __tablename__ = 'Empleados'

    empleado_id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    rol = Column(Enum('Gerente', 'Vendedor', 'Almacenista', name='rol_empleado'), nullable=False)
    email = Column(String(100), unique=True)
    telefono = Column(String(20))
    fecha_contratacion = Column(Date, nullable=False)
    salario = Column(Float)

    ventas = relationship("Venta", back_populates="empleado")