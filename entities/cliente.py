from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'Clientes'
    
    cliente_id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    telefono = Column(String(20))
    direccion = Column(Text)
    fecha_nacimiento = Column(Date)
    fecha_registro = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    tipo_cliente = Column(Enum('Regular', 'Premium', name='tipo_cliente'), default='Regular')