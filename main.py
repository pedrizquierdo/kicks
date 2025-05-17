from persistence.db import get_db, create_tables
from services.cliente_service import ClienteService
from services.producto_service import ProductoService

# Crear tablas si no existen
create_tables()

# Obtener sesión de base de datos
db = next(get_db())

# Ejemplo de uso del servicio de clientes
cliente_service = ClienteService(db)

# Crear un nuevo cliente
nuevo_cliente = {
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan.perez@example.com",
    "telefono": "5551234567",
    "tipo_cliente": "Premium"
}
cliente_creado = cliente_service.create_cliente(nuevo_cliente)
print(f"Cliente creado: {cliente_creado.nombre} {cliente_creado.apellido}")

# Listar todos los clientes
clientes = cliente_service.get_clientes()
print("\nLista de clientes:")
for cliente in clientes:
    print(f"{cliente.cliente_id}: {cliente.nombre} {cliente.apellido} - {cliente.tipo_cliente}")

# Ejemplo de uso del servicio de productos
producto_service = ProductoService(db)

# Crear un nuevo producto
nuevo_producto = {
    "nombre": "Zapatillas Running Pro",
    "precio": 89.99,
    "costo": 45.50,
    "marca_id": 1,
    "categoria_id": 1,
    "genero": "Hombre",
    "temporada": "All Season"
}
producto_creado = producto_service.create_producto(nuevo_producto)
print(f"\nProducto creado: {producto_creado.nombre} - ${producto_creado.precio}")

# Listar todos los productos
productos = producto_service.get_productos()
print("\nLista de productos:")
for producto in productos:
    print(f"{producto.producto_id}: {producto.nombre} - ${producto.precio}")
    