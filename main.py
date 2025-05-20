from persistence.db import get_db, create_tables
from services.cliente_service import ClienteService
from services.producto_service import ProductoService
from services.colores_service import ColorService
from services.tallas_service import TallaService
from services.marcas_service import MarcaService
from services.proveedor_service import ProveedorService
from services.empleados_service import EmpleadoService
from services.ventas_service import VentaService
from services.detalle_ventas_service import DetalleVentaService
from services.compras_service import CompraService
from services.detalle_compras_service import DetalleCompraService
from services.resenas_service import ResenaService
from services.promociones_service import PromocionService

TIPOS_CLIENTE = ['Regular', 'Premium']
GENEROS = ['Hombre', 'Mujer', 'Unisex', 'Niño', 'Niña']
TEMPORADAS = ['Verano', 'Invierno', 'Primavera', 'Otoño', 'All Season']

create_tables()
db = next(get_db())

cliente_service = ClienteService(db)
producto_service = ProductoService(db)
color_service = ColorService(db)
talla_service = TallaService(db)
marca_service = MarcaService(db)
proveedor_service = ProveedorService(db)
empleado_service = EmpleadoService(db)
venta_service = VentaService(db)
detalle_venta_service = DetalleVentaService(db)
compra_service = CompraService(db)
detalle_compra_service = DetalleCompraService(db)
resena_service = ResenaService(db)
promocion_service = PromocionService(db)

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
    print("\n--- Menú General ---")
    print("1. Crear cliente")
    print("2. Crear producto")
    print("3. Crear empleado")
    print("4. Crear proveedor")
    print("5. Crear venta")
    print("6. Crear compra")
    print("7. Crear reseña")
    print("8. Crear promoción")
    print("9. Crear color")
    print("10. Crear talla")
    print("11. Crear marca")
    print("12. Listar clientes")
    print("13. Listar productos")
    print("14. Listar empleados")
    print("15. Listar proveedores")
    print("16. Listar ventas")
    print("17. Listar compras")
    print("18. Listar reseñas")
    print("19. Listar promociones")
    print("20. Listar colores")
    print("21. Listar tallas")
    print("22. Listar marcas")
    print("23. Salir")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        nombre = pedir_input("Nombre: ")
        apellido = pedir_input("Apellido: ")
        email = pedir_input("Email: ")
        telefono = pedir_input("Teléfono: ")
        tipo_cliente = pedir_input("Tipo de cliente: ", opciones=TIPOS_CLIENTE)
        data = {"nombre": nombre, "apellido": apellido, "email": email, "telefono": telefono, "tipo_cliente": tipo_cliente}
        try:
            cliente = cliente_service.create_cliente(data)
            print(f"Cliente creado: {cliente.nombre} {cliente.apellido}")
        except Exception as e:
            db.rollback()
            print("Error al crear cliente:", e)

    elif opcion == "2":
        nombre = pedir_input("Nombre del producto: ")
        precio = pedir_input("Precio: ", tipo=float)
        costo = pedir_input("Costo: ", tipo=float)
        marca_id = pedir_input("ID de marca: ", tipo=int)
        categoria_id = pedir_input("ID de categoría: ", tipo=int)
        genero = pedir_input("Género: ", opciones=GENEROS)
        temporada = pedir_input("Temporada: ", opciones=TEMPORADAS)
        data = {"nombre": nombre, "precio": precio, "costo": costo, "marca_id": marca_id, "categoria_id": categoria_id, "genero": genero, "temporada": temporada}
        try:
            producto = producto_service.create_producto(data)
            print(f"Producto creado: {producto.nombre} - ${producto.precio}")
        except Exception as e:
            db.rollback()
            print("Error al crear producto:", e)

    elif opcion == "3":
        nombre = pedir_input("Nombre: ")
        apellido = pedir_input("Apellido: ")
        puesto = pedir_input("Puesto: ", opciones=["Vendedor", "Almacenista", "Gerente"])
        email = pedir_input("Email: ")
        telefono = pedir_input("Teléfono: ")
        fecha_contratacion = pedir_input("Fecha de contratación (YYYY-MM-DD): ")
        salario = pedir_input("Salario: ", tipo=float)
        data = {"nombre": nombre, "apellido": apellido, "puesto": puesto, "email": email, "telefono": telefono, "fecha_contratacion": fecha_contratacion, "salario": salario}
        try:
            empleado = empleado_service.create_empleado(data)
            print(f"Empleado creado: {empleado.nombre} {empleado.apellido}")
        except Exception as e:
            db.rollback()
            print("Error al crear empleado:", e)

    elif opcion == "4":
        nombre = pedir_input("Nombre del proveedor: ")
        contacto = pedir_input("Nombre del contacto: ")
        telefono = pedir_input("Teléfono: ")
        email = pedir_input("Email: ")
        direccion = pedir_input("Dirección: ")
        tipo_producto = pedir_input("Tipo de producto: ", opciones=["Calzado", "Ropa", "Ambos"])
        data = {"nombre": nombre, "contacto": contacto, "telefono": telefono, "email": email, "direccion": direccion, "tipo_producto": tipo_producto}
        try:
            proveedor = proveedor_service.create_proveedor(data)
            print(f"Proveedor creado: {proveedor.nombre}")
        except Exception as e:
            db.rollback()
            print("Error al crear proveedor:", e)
    elif opcion == "5":
        cliente_id = pedir_input("ID del cliente: ", tipo=int)
        empleado_id = pedir_input("ID del empleado: ", tipo=int)
        total = pedir_input("Total de la venta: ", tipo=float)
        metodo_pago = pedir_input("Método de pago: ", opciones=["Efectivo", "Tarjeta", "Transferencia"])
        estado = pedir_input("Estado: ", opciones=["Completada", "Cancelada", "En proceso"])
        data = {"cliente_id": cliente_id, "empleado_id": empleado_id, "total": total, "metodo_pago": metodo_pago, "estado": estado}
        try:
            venta = venta_service.create_venta(data)
            print(f"Venta creada con ID: {venta.venta_id}")
        except Exception as e:
            db.rollback()
            print("Error al crear venta:", e)

    elif opcion == "6":
        proveedor_id = pedir_input("ID del proveedor: ", tipo=int)
        total = pedir_input("Total de la compra: ", tipo=float)
        estado = pedir_input("Estado: ", opciones=["Pendiente", "Recibido", "Cancelado"])
        data = {"proveedor_id": proveedor_id, "total": total, "estado": estado}
        try:
            compra = compra_service.create_compra(data)
            print(f"Compra creada con ID: {compra.compra_id}")
        except Exception as e:
            db.rollback()
            print("Error al crear compra:", e)

    elif opcion == "7":
        producto_id = pedir_input("ID del producto: ", tipo=int)
        cliente_id = pedir_input("ID del cliente: ", tipo=int)
        calificacion = pedir_input("Calificación (1-5): ", tipo=int)
        comentario = pedir_input("Comentario: ")
        data = {"producto_id": producto_id, "cliente_id": cliente_id, "calificacion": calificacion, "comentario": comentario}
        try:
            resena = resena_service.create_resena(data)
            print(f"Reseña creada con ID: {resena.resena_id}")
        except Exception as e:
            db.rollback()
            print("Error al crear reseña:", e)

    elif opcion == "8":
        nombre = pedir_input("Nombre de la promoción: ")
        descripcion = pedir_input("Descripción: ")
        descuento = pedir_input("Descuento (%): ", tipo=float)
        fecha_inicio = pedir_input("Fecha de inicio (YYYY-MM-DD): ")
        fecha_fin = pedir_input("Fecha de fin (YYYY-MM-DD): ")
        productos_aplicables = pedir_input("Productos aplicables: ", opciones=["Todos", "Categoría específica", "Marca específica"])
        categoria_id = pedir_input("ID de categoría (opcional, enter para saltar): ", obligatorio=False)
        marca_id = pedir_input("ID de marca (opcional, enter para saltar): ", obligatorio=False)
        data = {"nombre": nombre, "descripcion": descripcion, "descuento_porcentaje": descuento, "fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin, "productos_aplicables": productos_aplicables, "categoria_id": int(categoria_id) if categoria_id else None, "marca_id": int(marca_id) if marca_id else None}
        try:
            promo = promocion_service.create_promocion(data)
            print(f"Promoción creada: {promo.nombre}")
        except Exception as e:
            db.rollback()
            print("Error al crear promoción:", e)

    elif opcion == "9":
        nombre = pedir_input("Nombre del color: ")
        codigo_hex = pedir_input("Código HEX del color (#xxxxxx): ")
        data = {"nombre": nombre, "codigo_hex": codigo_hex}
        try:
            color = color_service.create_color(data)
            print(f"Color creado: {color.nombre}")
        except Exception as e:
            db.rollback()
            print("Error al crear color:", e)

    elif opcion == "10":
        tipo = pedir_input("Tipo (Calzado/Ropa): ", opciones=["Calzado", "Ropa"])
        valor = pedir_input("Valor: ")
        descripcion = pedir_input("Descripción: ")
        data = {"tipo": tipo, "valor": valor, "descripcion": descripcion}
        try:
            talla = talla_service.create_talla(data)
            print(f"Talla creada: {talla.valor}")
        except Exception as e:
            db.rollback()
            print("Error al crear talla:", e)

    elif opcion == "11":
        nombre = pedir_input("Nombre de la marca: ")
        descripcion = pedir_input("Descripción: ")
        pais = pedir_input("País de origen: ")
        web = pedir_input("Sitio web: ")
        data = {"nombre": nombre, "descripcion": descripcion, "pais_origen": pais, "sitio_web": web}
        try:
            marca = marca_service.create_marca(data)
            print(f"Marca creada: {marca.nombre}")
        except Exception as e:
            db.rollback()
            print("Error al crear marca:", e)

    elif opcion == "12":
        for c in cliente_service.get_clientes(): print(f"{c.cliente_id}: {c.nombre} {c.apellido} - {c.tipo_cliente}")
    elif opcion == "13":
        for p in producto_service.get_productos(): print(f"{p.producto_id}: {p.nombre} - ${p.precio}")
    elif opcion == "14":
        for e in empleado_service.get_empleados(): print(f"{e.empleado_id}: {e.nombre} {e.apellido} - {e.puesto}")
    elif opcion == "15":
        for p in proveedor_service.get_proveedores(): print(f"{p.proveedor_id}: {p.nombre} - {p.tipo_producto}")
    elif opcion == "16":
        for v in venta_service.get_ventas(): print(f"{v.venta_id}: Cliente {v.cliente_id} - Total ${v.total}")
    elif opcion == "17":
        for c in compra_service.get_compras(): print(f"{c.compra_id}: Proveedor {c.proveedor_id} - Total ${c.total}")
    elif opcion == "18":
        for r in resena_service.get_resenas(): print(f"{r.resena_id}: Producto {r.producto_id} - Calificación {r.calificacion}")
    elif opcion == "19":
        for p in promocion_service.get_promociones(): print(f"{p.promocion_id}: {p.nombre} - {p.descuento_porcentaje}%")
    elif opcion == "20":
        for c in color_service.get_colores(): print(f"{c.color_id}: {c.nombre} ({c.codigo_hex})")
    elif opcion == "21":
        for t in talla_service.get_tallas(): print(f"{t.talla_id}: {t.tipo} - {t.valor}")
    elif opcion == "22":
        for m in marca_service.get_marcas(): print(f"{m.marca_id}: {m.nombre}")


    elif opcion == "23":
        print("Saliendo...")
        break

    else:
        print("Opción no válida. Intente de nuevo.")