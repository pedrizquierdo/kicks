import tkinter as tk
from tkinter import ttk, messagebox

from services.cliente_service import ClienteService
from services.producto_service import ProductoService
from services.colores_service import ColorService
from services.tallas_service import TallaService
from services.marcas_service import MarcaService
from services.proveedor_service import ProveedorService
from services.empleados_service import EmpleadoService
from services.ventas_service import VentaService
from services.compras_service import CompraService
from services.resenas_service import ResenaService
from services.promociones_service import PromocionService
from persistence.db import get_db

TIPOS_CLIENTE = ['Regular', 'Premium']
GENEROS = ['Hombre', 'Mujer', 'Unisex', 'Niño', 'Niña']
TEMPORADAS = ['Verano', 'Invierno', 'Primavera', 'Otoño', 'All Season']



class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menú General - Tienda Deportiva")
        self.geometry("400x650")
        self.resizable(False, True)

        ttk.Label(self, text="Menú General", font=("Arial", 18, "bold")).pack(pady=10)

        actions = [
            ("Crear cliente", self.crear_cliente),
            ("Crear producto", self.crear_producto),
            ("Crear empleado", self.crear_empleado),
            ("Crear proveedor", self.crear_proveedor),
            ("Crear venta", self.crear_venta),
            ("Crear compra", self.crear_compra),
            ("Crear reseña", self.crear_resena),
            ("Crear promoción", self.crear_promocion),
            ("Crear color", self.crear_color),
            ("Crear talla", self.crear_talla),
            ("Crear marca", self.crear_marca),
            ("Listar clientes", self.listar_clientes),
            ("Listar productos", self.listar_productos),
            ("Listar empleados", self.listar_empleados),
            ("Listar proveedores", self.listar_proveedores),
            ("Listar ventas", self.listar_ventas),
            ("Listar compras", self.listar_compras),
            ("Listar reseñas", self.listar_resenas),
            ("Listar promociones", self.listar_promociones),
            ("Listar colores", self.listar_colores),
            ("Listar tallas", self.listar_tallas),
            ("Listar marcas", self.listar_marcas),
            ("Salir", self.quit)
        ]

        for text, command in actions:
            ttk.Button(self, text=text, command=command).pack(fill="x", padx=20, pady=3)

    def crear_cliente(self):
        win = tk.Toplevel(self)
        win.title("Crear cliente")
        win.geometry("300x350")
        labels = ["Nombre", "Apellido", "Email", "Teléfono", "Tipo de cliente"]
        entries = []
        for i, label in enumerate(labels):
            ttk.Label(win, text=label).pack()
            if label == "Tipo de cliente":
                var = tk.StringVar(value=TIPOS_CLIENTE[0])
                cb = ttk.Combobox(win, values=TIPOS_CLIENTE, textvariable=var, state="readonly")
                cb.pack()
                entries.append(var)
            else:
                var = tk.StringVar()
                ttk.Entry(win, textvariable=var).pack()
                entries.append(var)
        def guardar():
            data = {
                "nombre": entries[0].get(),
                "apellido": entries[1].get(),
                "email": entries[2].get(),
                "telefono": entries[3].get(),
                "tipo_cliente": entries[4].get()
            }
            try:
                with next(get_db()) as db:
                    cliente_service = ClienteService(db)
                    cliente = cliente_service.create_cliente(data)
                messagebox.showinfo("Éxito", f"Cliente creado: {cliente.nombre} {cliente.apellido}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear cliente: {e}")
        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def listar_clientes(self):
        win = tk.Toplevel(self)
        win.title("Lista de clientes")
        win.geometry("400x400")
        tree = ttk.Treeview(win, columns=("ID", "Nombre", "Apellido", "Tipo"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Apellido", text="Apellido")
        tree.heading("Tipo", text="Tipo")
        tree.pack(fill="both", expand=True)
        with next(get_db()) as db:
            cliente_service = ClienteService(db)
            clientes = cliente_service.get_clientes()
            for c in clientes:
                tree.insert("", "end", values=(c.cliente_id, c.nombre, c.apellido, c.tipo_cliente))

    # Puedes implementar los demás métodos siguiendo el mismo patrón:
    def crear_producto(self):
        win = tk.Toplevel(self)
        win.title("Crear producto")
        win.geometry("350x400")
        labels = ["Nombre", "Precio", "Costo", "ID de marca", "ID de categoría", "Género", "Temporada"]
        entries = []
        for label in labels:
            ttk.Label(win, text=label).pack()
            if label == "Género":
                var = tk.StringVar(value=GENEROS[0])
                cb = ttk.Combobox(win, values=GENEROS, textvariable=var, state="readonly")
                cb.pack()
                entries.append(var)
            elif label == "Temporada":
                var = tk.StringVar(value=TEMPORADAS[0])
                cb = ttk.Combobox(win, values=TEMPORADAS, textvariable=var, state="readonly")
                cb.pack()
                entries.append(var)
            else:
                var = tk.StringVar()
                ttk.Entry(win, textvariable=var).pack()
                entries.append(var)
        def guardar():
            try:
                data = {
                    "nombre": entries[0].get(),
                    "precio": float(entries[1].get()),
                    "costo": float(entries[2].get()),
                    "marca_id": int(entries[3].get()),
                    "categoria_id": int(entries[4].get()),
                    "genero": entries[5].get(),
                    "temporada": entries[6].get()
                }
                with next(get_db()) as db:
                    producto_service = ProductoService(db)
                    producto = producto_service.create_producto(data)
                messagebox.showinfo("Éxito", f"Producto creado: {producto.nombre} - ${producto.precio}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear producto: {e}")
        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def listar_productos(self):
        win = tk.Toplevel(self)
        win.title("Lista de productos")
        win.geometry("700x400")
        tree = ttk.Treeview(win, columns=("ID", "Nombre", "Precio", "Costo", "Marca", "Categoría", "Género", "Temporada"), show="headings")
        for col in ("ID", "Nombre", "Precio", "Costo", "Marca", "Categoría", "Género", "Temporada"):
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)
        with next(get_db()) as db:
            producto_service = ProductoService(db)
            for p in producto_service.get_productos():
                tree.insert("", "end", values=(p.producto_id, p.nombre, p.precio, p.costo, p.marca_id, p.categoria_id, p.genero, p.temporada))

    def crear_empleado(self):
        win = tk.Toplevel(self)
        win.title("Crear empleado")
        win.geometry("350x400")
        labels = ["Nombre", "Apellido", "Puesto", "Email", "Teléfono", "Fecha de contratación (YYYY-MM-DD)", "Salario"]
        puestos = ["Vendedor", "Almacenista", "Gerente"]
        entries = []
        for label in labels:
            ttk.Label(win, text=label).pack()
            if label == "Puesto":
                var = tk.StringVar(value=puestos[0])
                cb = ttk.Combobox(win, values=puestos, textvariable=var, state="readonly")
                cb.pack()
                entries.append(var)
            else:
                var = tk.StringVar()
                ttk.Entry(win, textvariable=var).pack()
                entries.append(var)
        def guardar():
            try:
                data = {
                    "nombre": entries[0].get(),
                    "apellido": entries[1].get(),
                    "puesto": entries[2].get(),
                    "email": entries[3].get(),
                    "telefono": entries[4].get(),
                    "fecha_contratacion": entries[5].get(),
                    "salario": float(entries[6].get())
                }
                with next(get_db()) as db:
                    empleado_service = EmpleadoService(db)
                    empleado = empleado_service.create_empleado(data)
                messagebox.showinfo("Éxito", f"Empleado creado: {empleado.nombre} {empleado.apellido}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear empleado: {e}")
        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def listar_empleados(self):
        win = tk.Toplevel(self)
        win.title("Lista de empleados")
        win.geometry("600x400")
        tree = ttk.Treeview(win, columns=("ID", "Nombre", "Apellido", "Puesto", "Email", "Teléfono", "Fecha contratación", "Salario"), show="headings")
        for col in ("ID", "Nombre", "Apellido", "Puesto", "Email", "Teléfono", "Fecha contratación", "Salario"):
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)
        with next(get_db()) as db:
            empleado_service = EmpleadoService(db)
            for e in empleado_service.get_empleados():
                tree.insert("", "end", values=(e.empleado_id, e.nombre, e.apellido, e.puesto, e.email, e.telefono, e.fecha_contratacion, e.salario))

    def crear_proveedor(self):
        win = tk.Toplevel(self)
        win.title("Crear proveedor")
        win.geometry("350x400")
        labels = ["Nombre", "Nombre del contacto", "Teléfono", "Email", "Dirección", "Tipo de producto"]
        tipos = ["Calzado", "Ropa", "Ambos"]
        entries = []
        for label in labels:
            ttk.Label(win, text=label).pack()
            if label == "Tipo de producto":
                var = tk.StringVar(value=tipos[0])
                cb = ttk.Combobox(win, values=tipos, textvariable=var, state="readonly")
                cb.pack()
                entries.append(var)
            else:
                var = tk.StringVar()
                ttk.Entry(win, textvariable=var).pack()
                entries.append(var)
        def guardar():
            try:
                data = {
                    "nombre": entries[0].get(),
                    "contacto": entries[1].get(),
                    "telefono": entries[2].get(),
                    "email": entries[3].get(),
                    "direccion": entries[4].get(),
                    "tipo_producto": entries[5].get()
                }
                with next(get_db()) as db:
                    proveedor_service = ProveedorService(db)
                    proveedor = proveedor_service.create_proveedor(data)
                messagebox.showinfo("Éxito", f"Proveedor creado: {proveedor.nombre}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear proveedor: {e}")
        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def listar_proveedores(self):
        win = tk.Toplevel(self)
        win.title("Lista de proveedores")
        win.geometry("600x400")
        tree = ttk.Treeview(win, columns=("ID", "Nombre", "Contacto", "Teléfono", "Email", "Dirección", "Tipo producto"), show="headings")
        for col in ("ID", "Nombre", "Contacto", "Teléfono", "Email", "Dirección", "Tipo producto"):
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)
        with next(get_db()) as db:
            proveedor_service = ProveedorService(db)
            for p in proveedor_service.get_proveedores():
                tree.insert("", "end", values=(p.proveedor_id, p.nombre, p.contacto, p.telefono, p.email, p.direccion, p.tipo_producto))

    def crear_venta(self):
        win = tk.Toplevel(self)
        win.title("Crear venta")
        win.geometry("350x400")
        labels = ["ID del cliente", "ID del empleado", "Total", "Método de pago", "Estado"]
        metodos = ["Efectivo", "Tarjeta", "Transferencia"]
        estados = ["Completada", "Cancelada", "En proceso"]
        entries = []
        for label in labels:
            ttk.Label(win, text=label).pack()
            if label == "Método de pago":
                var = tk.StringVar(value=metodos[0])
                cb = ttk.Combobox(win, values=metodos, textvariable=var, state="readonly")
                cb.pack()
                entries.append(var)
            elif label == "Estado":
                var = tk.StringVar(value=estados[0])
                cb = ttk.Combobox(win, values=estados, textvariable=var, state="readonly")
                cb.pack()
                entries.append(var)
            else:
                var = tk.StringVar()
                ttk.Entry(win, textvariable=var).pack()
                entries.append(var)
        def guardar():
            try:
                data = {
                    "cliente_id": int(entries[0].get()),
                    "empleado_id": int(entries[1].get()),
                    "total": float(entries[2].get()),
                    "metodo_pago": entries[3].get(),
                    "estado": entries[4].get()
                }
                with next(get_db()) as db:
                    venta_service = VentaService(db)
                    venta = venta_service.create_venta(data)
                messagebox.showinfo("Éxito", f"Venta creada con ID: {venta.venta_id}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear venta: {e}")
        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def listar_ventas(self):
        win = tk.Toplevel(self)
        win.title("Lista de ventas")
        win.geometry("700x400")
        tree = ttk.Treeview(win, columns=("ID", "Cliente", "Empleado", "Total", "Método pago", "Estado"), show="headings")
        for col in ("ID", "Cliente", "Empleado", "Total", "Método pago", "Estado"):
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)
        with next(get_db()) as db:
            venta_service = VentaService(db)
            for v in venta_service.get_ventas():
                tree.insert("", "end", values=(v.venta_id, v.cliente_id, v.empleado_id, v.total, v.metodo_pago, v.estado))

    def crear_compra(self):
        win = tk.Toplevel(self)
        win.title("Crear compra")
        win.geometry("350x300")
        labels = ["ID del proveedor", "Total", "Estado"]
        estados = ["Pendiente", "Recibido", "Cancelado"]
        entries = []
        for label in labels:
            ttk.Label(win, text=label).pack()
            if label == "Estado":
                var = tk.StringVar(value=estados[0])
                cb = ttk.Combobox(win, values=estados, textvariable=var, state="readonly")
                cb.pack()
                entries.append(var)
            else:
                var = tk.StringVar()
                ttk.Entry(win, textvariable=var).pack()
                entries.append(var)
        def guardar():
            try:
                data = {
                    "proveedor_id": int(entries[0].get()),
                    "total": float(entries[1].get()),
                    "estado": entries[2].get()
                }
                with next(get_db()) as db:
                    compra_service = CompraService(db)
                    compra = compra_service.create_compra(data)
                messagebox.showinfo("Éxito", f"Compra creada con ID: {compra.compra_id}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear compra: {e}")
        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def listar_compras(self):
        win = tk.Toplevel(self)
        win.title("Lista de compras")
        win.geometry("700x400")
        tree = ttk.Treeview(win, columns=("ID", "Proveedor", "Total", "Estado"), show="headings")
        for col in ("ID", "Proveedor", "Total", "Estado"):
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)
        with next(get_db()) as db:
            compra_service = CompraService(db)
            for c in compra_service.get_compras():
                tree.insert("", "end", values=(c.compra_id, c.proveedor_id, c.total, c.estado))

    def crear_resena(self):
        win = tk.Toplevel(self)
        win.title("Crear reseña")
        win.geometry("350x300")
        labels = ["ID del producto", "ID del cliente", "Calificación (1-5)", "Comentario"]
        entries = []
        for label in labels:
            ttk.Label(win, text=label).pack()
            var = tk.StringVar()
            ttk.Entry(win, textvariable=var).pack()
            entries.append(var)
        def guardar():
            try:
                data = {
                    "producto_id": int(entries[0].get()),
                    "cliente_id": int(entries[1].get()),
                    "calificacion": int(entries[2].get()),
                    "comentario": entries[3].get()
                }
                with next(get_db()) as db:
                    resena_service = ResenaService(db)
                    resena = resena_service.create_resena(data)
                messagebox.showinfo("Éxito", f"Reseña creada con ID: {resena.resena_id}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear reseña: {e}")
        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def listar_resenas(self):
        win = tk.Toplevel(self)
        win.title("Lista de reseñas")
        win.geometry("700x400")
        tree = ttk.Treeview(win, columns=("ID", "Producto", "Cliente", "Calificación", "Comentario"), show="headings")
        for col in ("ID", "Producto", "Cliente", "Calificación", "Comentario"):
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)
        with next(get_db()) as db:
            resena_service = ResenaService(db)
            for r in resena_service.get_resenas():
                tree.insert("", "end", values=(r.resena_id, r.producto_id, r.cliente_id, r.calificacion, r.comentario))

    def crear_promocion(self):
        win = tk.Toplevel(self)
        win.title("Crear promoción")
        win.geometry("400x400")
        labels = ["Nombre", "Descripción", "Descuento (%)", "Fecha de inicio (YYYY-MM-DD)", "Fecha de fin (YYYY-MM-DD)", "Productos aplicables", "ID de categoría (opcional)", "ID de marca (opcional)"]
        productos_aplicables = ["Todos", "Categoría específica", "Marca específica"]
        entries = []
        for label in labels:
            ttk.Label(win, text=label).pack()
            if label == "Productos aplicables":
                var = tk.StringVar(value=productos_aplicables[0])
                cb = ttk.Combobox(win, values=productos_aplicables, textvariable=var, state="readonly")
                cb.pack()
                entries.append(var)
            else:
                var = tk.StringVar()
                ttk.Entry(win, textvariable=var).pack()
                entries.append(var)
        def guardar():
            try:
                data = {
                    "nombre": entries[0].get(),
                    "descripcion": entries[1].get(),
                    "descuento_porcentaje": float(entries[2].get()),
                    "fecha_inicio": entries[3].get(),
                    "fecha_fin": entries[4].get(),
                    "productos_aplicables": entries[5].get(),
                    "categoria_id": int(entries[6].get()) if entries[6].get() else None,
                    "marca_id": int(entries[7].get()) if entries[7].get() else None
                }
                with next(get_db()) as db:
                    promo_service = PromocionService(db)
                    promo = promo_service.create_promocion(data)
                messagebox.showinfo("Éxito", f"Promoción creada: {promo.nombre}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear promoción: {e}")
        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def listar_promociones(self):
        win = tk.Toplevel(self)
        win.title("Lista de promociones")
        win.geometry("700x400")
        tree = ttk.Treeview(win, columns=("ID", "Nombre", "Descuento %", "Inicio", "Fin", "Aplicable", "CatID", "MarcaID"), show="headings")
        for col in ("ID", "Nombre", "Descuento %", "Inicio", "Fin", "Aplicable", "CatID", "MarcaID"):
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)
        with next(get_db()) as db:
            promocion_service = PromocionService(db)
            for p in promocion_service.get_promociones():
                tree.insert("", "end", values=(p.promocion_id, p.nombre, p.descuento_porcentaje, p.fecha_inicio, p.fecha_fin, p.productos_aplicables, p.categoria_id, p.marca_id))

    def crear_color(self):
        win = tk.Toplevel(self)
        win.title("Crear color")
        win.geometry("300x200")
        labels = ["Nombre", "Código HEX"]
        entries = []
        for label in labels:
            ttk.Label(win, text=label).pack()
            var = tk.StringVar()
            ttk.Entry(win, textvariable=var).pack()
            entries.append(var)
        def guardar():
            try:
                data = {
                    "nombre": entries[0].get(),
                    "codigo_hex": entries[1].get()
                }
                with next(get_db()) as db:
                    color_service = ColorService(db)
                    color = color_service.create_color(data)
                messagebox.showinfo("Éxito", f"Color creado: {color.nombre}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear color: {e}")
        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def listar_colores(self):
        win = tk.Toplevel(self)
        win.title("Lista de colores")
        win.geometry("400x400")
        tree = ttk.Treeview(win, columns=("ID", "Nombre", "HEX"), show="headings")
        for col in ("ID", "Nombre", "HEX"):
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)
        with next(get_db()) as db:
            color_service = ColorService(db)
            for c in color_service.get_colores():
                tree.insert("", "end", values=(c.color_id, c.nombre, c.codigo_hex))

    def crear_talla(self):
        win = tk.Toplevel(self)
        win.title("Crear talla")
        win.geometry("300x250")
        labels = ["Tipo (Calzado/Ropa)", "Valor", "Descripción"]
        tipos = ["Calzado", "Ropa"]
        entries = []
        for label in labels:
            ttk.Label(win, text=label).pack()
            if label == "Tipo (Calzado/Ropa)":
                var = tk.StringVar(value=tipos[0])
                cb = ttk.Combobox(win, values=tipos, textvariable=var, state="readonly")
                cb.pack()
                entries.append(var)
            else:
                var = tk.StringVar()
                ttk.Entry(win, textvariable=var).pack()
                entries.append(var)
        def guardar():
            try:
                data = {
                    "tipo": entries[0].get(),
                    "valor": entries[1].get(),
                    "descripcion": entries[2].get()
                }
                with next(get_db()) as db:
                    talla_service = TallaService(db)
                    talla = talla_service.create_talla(data)
                messagebox.showinfo("Éxito", f"Talla creada: {talla.valor}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear talla: {e}")
        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def listar_tallas(self):
        win = tk.Toplevel(self)
        win.title("Lista de tallas")
        win.geometry("400x400")
        tree = ttk.Treeview(win, columns=("ID", "Tipo", "Valor", "Descripción"), show="headings")
        for col in ("ID", "Tipo", "Valor", "Descripción"):
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)
        with next(get_db()) as db:
            talla_service = TallaService(db)
            for t in talla_service.get_tallas():
                tree.insert("", "end", values=(t.talla_id, t.tipo, t.valor, t.descripcion))

    def crear_marca(self):
        win = tk.Toplevel(self)
        win.title("Crear marca")
        win.geometry("350x250")
        labels = ["Nombre", "Descripción", "País de origen", "Sitio web"]
        entries = []
        for label in labels:
            ttk.Label(win, text=label).pack()
            var = tk.StringVar()
            ttk.Entry(win, textvariable=var).pack()
            entries.append(var)
        def guardar():
            try:
                data = {
                    "nombre": entries[0].get(),
                    "descripcion": entries[1].get(),
                    "pais_origen": entries[2].get(),
                    "sitio_web": entries[3].get()
                }
                with next(get_db()) as db:
                    marca_service = MarcaService(db)
                    marca = marca_service.create_marca(data)
                messagebox.showinfo("Éxito", f"Marca creada: {marca.nombre}")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear marca: {e}")
        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def listar_marcas(self):
        win = tk.Toplevel(self)
        win.title("Lista de marcas")
        win.geometry("500x400")
        tree = ttk.Treeview(win, columns=("ID", "Nombre", "Descripción", "País", "Web"), show="headings")
        for col in ("ID", "Nombre", "Descripción", "País", "Web"):
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)
        with next(get_db()) as db:
            marca_service = MarcaService(db)
            for m in marca_service.get_marcas():
                tree.insert("", "end", values=(m.marca_id, m.nombre, m.descripcion, m.pais_origen, m.sitio_web))
# Para ejecutar la interfaz gráfica desde otro archivo:
def run_gui():
    app = MainMenu()
    app.mainloop()