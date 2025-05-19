from persistence.db import get_db, create_tables
from services.cliente_service import ClienteService
from services.producto_service import ProductoService

# Opciones válidas para enums
TIPOS_CLIENTE = ['Regular', 'Premium']
GENEROS = ['Hombre', 'Mujer', 'Unisex', 'Niño', 'Niña']
TEMPORADAS = ['Verano', 'Invierno', 'Primavera', 'Otoño', 'All Season']

# Crear tablas si no existen
create_tables()

# Obtener sesión de base de datos
db = next(get_db())

cliente_service = ClienteService(db)
producto_service = ProductoService(db)

def pedir_input(mensaje, tipo=str, opciones=None, obligatorio=True):
    while True:
        valor = input(mensaje)
        if obligatorio and not valor:
            print("El valor no puede estar vacío. Intente de nuevo.")
            continue
        if opciones and valor not in opciones:
            print(f"Opción inválida. Opciones válidas: {', '.join(opciones)}")
            continue
        if tipo == int:
            try:
                return int(valor)
            except ValueError:
                print("Debe ingresar un número entero válido.")
                continue
        elif tipo == float:
            try:
                return float(valor)
            except ValueError:
                print("Debe ingresar un número decimal válido.")
                continue
        else:
            return valor

while True:
    print("\n--- Menú ---")
    print("1. Crear cliente")
    print("2. Crear producto")
    print("3. Listar clientes")
    print("4. Listar productos")
    print("5. Salir")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        print("\nIngrese los datos del cliente:")
        nombre = pedir_input("Nombre: ")
        apellido = pedir_input("Apellido: ")
        email = pedir_input("Email: ")
        telefono = pedir_input("Teléfono: ")
        print(f"Tipo de cliente ({'/'.join(TIPOS_CLIENTE)}): ")
        tipo_cliente = pedir_input("Seleccione tipo: ", opciones=TIPOS_CLIENTE)
        nuevo_cliente = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "telefono": telefono,
            "tipo_cliente": tipo_cliente
        }
        try:
            cliente_creado = cliente_service.create_cliente(nuevo_cliente)
            print(f"Cliente creado: {cliente_creado.nombre} {cliente_creado.apellido}")
        except Exception as e:
            print(f"Error al crear cliente: {e}. Intente de nuevo.")

    elif opcion == "2":
        print("\nIngrese los datos del producto:")
        nombre = pedir_input("Nombre: ")
        precio = pedir_input("Precio: ", tipo=float)
        costo = pedir_input("Costo: ", tipo=float)
        marca_id = pedir_input("ID de marca: ", tipo=int)
        categoria_id = pedir_input("ID de categoría: ", tipo=int)
        print(f"Género ({'/'.join(GENEROS)}): ")
        genero = pedir_input("Seleccione género: ", opciones=GENEROS)
        print(f"Temporada ({'/'.join(TEMPORADAS)}): ")
        temporada = pedir_input("Seleccione temporada: ", opciones=TEMPORADAS)
        nuevo_producto = {
            "nombre": nombre,
            "precio": precio,
            "costo": costo,
            "marca_id": marca_id,
            "categoria_id": categoria_id,
            "genero": genero,
            "temporada": temporada
        }
        try:
            producto_creado = producto_service.create_producto(nuevo_producto)
            print(f"Producto creado: {producto_creado.nombre} - ${producto_creado.precio}")
        except Exception as e:
            print(f"Error al crear producto: {e}. Intente de nuevo.")

    elif opcion == "3":
        clientes = cliente_service.get_clientes()
        if not clientes:
            print("\nNo hay clientes registrados. Por favor, ingrese al menos un cliente primero.")
            continue
        print("\nLista de clientes:")
        for cliente in clientes:
            print(f"{cliente.cliente_id}: {cliente.nombre} {cliente.apellido} - {cliente.tipo_cliente}")

    elif opcion == "4":
        productos = producto_service.get_productos()
        if not productos:
            print("\nNo hay productos registrados. Por favor, ingrese al menos un producto primero.")
            continue
        print("\nLista de productos:")
        for producto in productos:
            print(f"{producto.producto_id}: {producto.nombre} - ${producto.precio}")

    elif opcion == "5":
        print("Saliendo...")
        break
    else:
        print("Opción no válida. Intente de nuevo.")
