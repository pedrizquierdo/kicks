from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuración de la conexión (ajusta según tu entorno)
CONNECTION = 'mysql+pymysql://root:Moonpiece@localhost:3308/tienda_deportiva'

# Crear el motor de la base de datos
engine = create_engine(CONNECTION, echo=True)

# Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear todas las tablas
def create_tables():
    from entities.categoria import Categoria
    from entities.cliente import Cliente
    from entities.producto import Producto
    from entities.marcas import Marca
    from entities.inventario import Inventario

