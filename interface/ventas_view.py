import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from services.marcas_service import MarcaService
from services.ventas_service import VentaService
from services.detalle_ventas_service import DetalleVentaService
from services.producto_service import ProductoService
from services.cliente_service import ClienteService
from services.empleados_service import EmpleadoService
from persistence.db import get_db
from datetime import datetime

class VentasView(tk.Toplevel):
    def __init__(self, parent, empleado):
        super().__init__(parent)
        self.title(f"Registro de Ventas - {empleado.nombre}")
        self.geometry("1000x700")
        
        self.empleado = empleado
        self.cliente = None
        self.productos_venta = []
        self.db = next(get_db())
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de información del cliente
        cliente_frame = ttk.LabelFrame(main_frame, text="Información del Cliente", padding=10)
        cliente_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(cliente_frame, text="Buscar Cliente", command=self.buscar_cliente).pack(side=tk.LEFT)
        self.cliente_info = ttk.Label(cliente_frame, text="No se ha seleccionado cliente")
        self.cliente_info.pack(side=tk.LEFT, padx=10)
        
        # Frame de búsqueda de productos
        search_frame = ttk.LabelFrame(main_frame, text="Buscar Producto", padding=10)
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="Buscar (ID o Nombre):").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        ttk.Button(search_frame, text="Buscar", command=self.buscar_productos).pack(side=tk.LEFT)
        
        # Treeview para productos
        self.productos_tree = ttk.Treeview(
            main_frame, 
            columns=("ID", "Nombre", "Marca", "Precio", "Stock"), 
            show="headings",
            height=8
        )
        self.productos_tree.heading("ID", text="ID")
        self.productos_tree.heading("Nombre", text="Nombre")
        self.productos_tree.heading("Marca", text="Marca")
        self.productos_tree.heading("Precio", text="Precio")
        self.productos_tree.heading("Stock", text="Stock")
        self.productos_tree.column("ID", width=50)
        self.productos_tree.column("Nombre", width=200)
        self.productos_tree.column("Marca", width=100)
        self.productos_tree.column("Precio", width=80)
        self.productos_tree.column("Stock", width=50)
        self.productos_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Frame para detalles de venta
        venta_frame = ttk.LabelFrame(main_frame, text="Detalles de Venta", padding=10)
        venta_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Treeview para productos seleccionados
        self.venta_tree = ttk.Treeview(
            venta_frame, 
            columns=("ID", "Nombre", "Precio", "Cantidad", "Subtotal"), 
            show="headings",
            height=6
        )
        self.venta_tree.heading("ID", text="ID")
        self.venta_tree.heading("Nombre", text="Nombre")
        self.venta_tree.heading("Precio", text="Precio")
        self.venta_tree.heading("Cantidad", text="Cantidad")
        self.venta_tree.heading("Subtotal", text="Subtotal")
        self.venta_tree.column("ID", width=50)
        self.venta_tree.column("Nombre", width=250)
        self.venta_tree.column("Precio", width=80)
        self.venta_tree.column("Cantidad", width=70)
        self.venta_tree.column("Subtotal", width=90)
        self.venta_tree.pack(fill=tk.BOTH, expand=True)
        
        # Frame para total y botones
        total_frame = ttk.Frame(venta_frame)
        total_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(total_frame, text="Total:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.total_var = tk.StringVar(value="$0.00")
        ttk.Label(total_frame, textvariable=self.total_var, font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        button_frame = ttk.Frame(venta_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Agregar Producto", command=self.agregar_a_venta).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Quitar Producto", command=self.quitar_de_venta).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Finalizar Venta", command=self.finalizar_venta).pack(side=tk.RIGHT, padx=5)
        
        # Cargar productos iniciales
        self.buscar_productos()
        
    def buscar_cliente(self):
        cliente_id = simpledialog.askinteger("Buscar Cliente", "Ingrese el ID del cliente:")
        if cliente_id:
            try:
                cliente_service = ClienteService(self.db)
                cliente = cliente_service.get_cliente_by_id(cliente_id)
                if cliente:
                    self.cliente = cliente
                    self.cliente_info.config(
                        text=f"Cliente: {cliente.nombre} {cliente.apellido} | Tel: {cliente.telefono} | Tipo: {cliente.tipo_cliente}"
                    )
                else:
                    messagebox.showwarning("Advertencia", "No se encontró un cliente con ese ID")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo buscar el cliente: {str(e)}")
    
    def buscar_productos(self):
        # Limpiar treeview
        for item in self.productos_tree.get_children():
            self.productos_tree.delete(item)
            
        search_term = self.search_entry.get()
        
        try:
            producto_service = ProductoService(self.db)
            
            if search_term:
                if search_term.isdigit():
                    # Buscar por ID
                    producto = producto_service.get_producto_by_id(int(search_term))
                    if producto:
                        productos = [producto]
                    else:
                        productos = []
                else:
                    # Buscar por nombre
                    productos = producto_service.buscar_productos_por_nombre(search_term)
            else:
                # Mostrar todos los productos
                productos = producto_service.get_productos()
                
            for prod in productos:
                # Obtener marca del producto
                marca_service = MarcaService(self.db)
                marca = marca_service.get_marca_by_id(prod.marca_id)
                
                # Aquí deberías obtener el stock real de la base de datos
                stock = 10  # Esto es un ejemplo, deberías obtenerlo del inventario
                
                self.productos_tree.insert("", tk.END, values=(
                    prod.producto_id,
                    prod.nombre,
                    marca.nombre if marca else "N/A",
                    f"${prod.precio:,.2f}",
                    stock
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la lista de productos: {str(e)}")
    
    def agregar_a_venta(self):
        selected = self.productos_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para agregar")
            return
            
        producto_data = self.productos_tree.item(selected[0])['values']
        producto_id = producto_data[0]
        nombre = producto_data[1]
        precio = float(producto_data[3].replace('$', '').replace(',', ''))
        
        # Pedir cantidad
        cantidad = simpledialog.askinteger("Cantidad", f"Ingrese la cantidad para {nombre}:", minvalue=1)
        if not cantidad:
            return
            
        # Verificar stock (deberías implementar esto correctamente)
        stock_disponible = int(producto_data[4])
        if cantidad > stock_disponible:
            messagebox.showwarning("Stock Insuficiente", f"No hay suficiente stock. Disponible: {stock_disponible}")
            return
            
        # Calcular subtotal
        subtotal = precio * cantidad
        
        # Agregar a la lista de productos
        self.productos_venta.append({
            'producto_id': producto_id,
            'nombre': nombre,
            'precio': precio,
            'cantidad': cantidad,
            'subtotal': subtotal
        })
        
        # Actualizar treeview de venta
        self.actualizar_venta_tree()
    
    def quitar_de_venta(self):
        selected = self.venta_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para quitar")
            return
            
        producto_id = int(self.venta_tree.item(selected[0])['values'][0])
        
        # Eliminar producto de la lista
        self.productos_venta = [p for p in self.productos_venta if p['producto_id'] != producto_id]
        
        # Actualizar treeview de venta
        self.actualizar_venta_tree()
    
    def actualizar_venta_tree(self):
        # Limpiar treeview
        for item in self.venta_tree.get_children():
            self.venta_tree.delete(item)
            
        # Agregar productos actualizados
        for prod in self.productos_venta:
            self.venta_tree.insert("", tk.END, values=(
                prod['producto_id'],
                prod['nombre'],
                f"${prod['precio']:,.2f}",
                prod['cantidad'],
                f"${prod['subtotal']:,.2f}"
            ))
        
        # Calcular y mostrar total
        total = sum(p['subtotal'] for p in self.productos_venta)
        self.total_var.set(f"${total:,.2f}")
    
    def finalizar_venta(self):
        if not self.cliente:
            messagebox.showwarning("Advertencia", "Debe seleccionar un cliente primero")
            return
            
        if not self.productos_venta:
            messagebox.showwarning("Advertencia", "No hay productos en la venta")
            return
            
        total = sum(p['subtotal'] for p in self.productos_venta)
        
        try:
            # Crear la venta en la base de datos
            venta_service = VentaService(self.db)
            venta_data = {
                'cliente_id': self.cliente.cliente_id,
                'empleado_id': self.empleado.empleado_id,
                'total': total,
                'metodo_pago': 'Efectivo',  # Podrías pedir este dato al usuario
                'estado': 'Completada'
            }
            venta = venta_service.create_venta(venta_data)
            
            # Crear los detalles de venta
            detalle_service = DetalleVentaService(self.db)
            for prod in self.productos_venta:
                detalle_data = {
                    'venta_id': venta.venta_id,
                    'producto_id': prod['producto_id'],
                    'cantidad': prod['cantidad'],
                    'precio_unitario': prod['precio'],
                    'descuento': 0,  # Podrías implementar descuentos
                    'subtotal': prod['subtotal']
                }
                detalle_service.create_detalle_venta(detalle_data)
            
            # Mostrar ticket
            self.mostrar_ticket(venta)
            
            # Limpiar venta actual
            self.productos_venta = []
            self.actualizar_venta_tree()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo completar la venta: {str(e)}")
    
    def mostrar_ticket(self, venta):
        ticket_window = tk.Toplevel(self)
        ticket_window.title(f"Ticket de Venta #{venta.venta_id}")
        ticket_window.geometry("400x600")
        
        # Frame principal
        main_frame = ttk.Frame(ticket_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Encabezado
        ttk.Label(main_frame, text="TIENDA DEPORTIVA", font=('Arial', 14, 'bold')).pack()
        ttk.Label(main_frame, text="Av. Principal 123, Hermosillo, Sonora", font=('Arial', 10)).pack()
        ttk.Label(main_frame, text="Tel: 662-123-4567", font=('Arial', 10)).pack()
        ttk.Label(main_frame, text="RFC: TDE123456ABC", font=('Arial', 10)).pack()
        
        # Separador
        ttk.Separator(main_frame).pack(fill=tk.X, pady=10)
        
        # Información de la venta
        ttk.Label(main_frame, text=f"Ticket: #{venta.venta_id}", font=('Arial', 10)).pack(anchor=tk.W)
        ttk.Label(main_frame, text=f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", font=('Arial', 10)).pack(anchor=tk.W)
        
        # Información del cliente
        ttk.Label(main_frame, text="Cliente:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10,0))
        ttk.Label(main_frame, text=f"{self.cliente.nombre} {self.cliente.apellido}", font=('Arial', 10)).pack(anchor=tk.W)
        ttk.Label(main_frame, text=f"Tipo: {self.cliente.tipo_cliente}", font=('Arial', 10)).pack(anchor=tk.W)
        
        # Información del vendedor
        ttk.Label(main_frame, text="Atendido por:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10,0))
        ttk.Label(main_frame, text=f"{self.empleado.nombre} {self.empleado.apellido}", font=('Arial', 10)).pack(anchor=tk.W)
        ttk.Label(main_frame, text=f"Rol: {self.empleado.rol}", font=('Arial', 10)).pack(anchor=tk.W)
        
        # Separador
        ttk.Separator(main_frame).pack(fill=tk.X, pady=10)
        
        # Detalle de productos
        ttk.Label(main_frame, text="Productos:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        for prod in self.productos_venta:
            product_frame = ttk.Frame(main_frame)
            product_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(product_frame, text=f"{prod['nombre']} x{prod['cantidad']}", font=('Arial', 9)).pack(side=tk.LEFT)
            ttk.Label(product_frame, text=f"${prod['subtotal']:,.2f}", font=('Arial', 9)).pack(side=tk.RIGHT)
        
        # Separador
        ttk.Separator(main_frame).pack(fill=tk.X, pady=10)
        
        # Total
        total_frame = ttk.Frame(main_frame)
        total_frame.pack(fill=tk.X)
        
        ttk.Label(total_frame, text="TOTAL:", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        ttk.Label(total_frame, text=f"${sum(p['subtotal'] for p in self.productos_venta):,.2f}", 
                 font=('Arial', 12, 'bold')).pack(side=tk.RIGHT)
        
        # Pie de ticket
        ttk.Separator(main_frame).pack(fill=tk.X, pady=10)
        ttk.Label(main_frame, text="¡Gracias por su compra!", font=('Arial', 10, 'italic')).pack()
        ttk.Label(main_frame, text="Devoluciones dentro de los 15 días con ticket", font=('Arial', 8)).pack()
        
        # Botón para imprimir o cerrar
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Imprimir", command=lambda: self.imprimir_ticket(ticket_window)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cerrar", command=ticket_window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def imprimir_ticket(self, window):
        # Aquí implementarías la lógica real de impresión
        messagebox.showinfo("Imprimir", "Ticket enviado a impresora")
        window.destroy()

