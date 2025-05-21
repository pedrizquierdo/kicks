import tkinter as tk
from tkinter import ttk, messagebox
from services.ventas_service import VentaService
from services.producto_service import ProductoService
from persistence.db import get_db

class VentasView(tk.Toplevel):
    def __init__(self, parent, empleado):
        super().__init__(parent)
        self.title(f"Registro de Ventas - {empleado.nombre}")
        self.geometry("900x600")
        
        self.empleado = empleado
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de búsqueda de productos
        search_frame = ttk.LabelFrame(main_frame, text="Buscar Producto", padding=10)
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        ttk.Button(search_frame, text="Buscar", command=self.buscar_productos).pack(side=tk.LEFT)
        
        # Treeview para productos
        self.productos_tree = ttk.Treeview(main_frame, columns=("ID", "Nombre", "Precio", "Stock"), show="headings")
        self.productos_tree.heading("ID", text="ID")
        self.productos_tree.heading("Nombre", text="Nombre")
        self.productos_tree.heading("Precio", text="Precio")
        self.productos_tree.heading("Stock", text="Stock")
        self.productos_tree.pack(fill=tk.BOTH, expand=True)
        
        # Frame para detalles de venta
        venta_frame = ttk.LabelFrame(main_frame, text="Detalles de Venta", padding=10)
        venta_frame.pack(fill=tk.X, pady=5)
        
        # Treeview para productos seleccionados
        self.venta_tree = ttk.Treeview(venta_frame, columns=("ID", "Nombre", "Precio", "Cantidad", "Subtotal"), show="headings")
        self.venta_tree.heading("ID", text="ID")
        self.venta_tree.heading("Nombre", text="Nombre")
        self.venta_tree.heading("Precio", text="Precio")
        self.venta_tree.heading("Cantidad", text="Cantidad")
        self.venta_tree.heading("Subtotal", text="Subtotal")
        self.venta_tree.pack(fill=tk.X)
        
        # Frame para total y botones
        total_frame = ttk.Frame(venta_frame)
        total_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(total_frame, text="Total:").pack(side=tk.LEFT)
        self.total_var = tk.StringVar(value="$0.00")
        ttk.Label(total_frame, textvariable=self.total_var, font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        button_frame = ttk.Frame(venta_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Agregar Producto", command=self.agregar_a_venta).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Quitar Producto", command=self.quitar_de_venta).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Finalizar Venta", command=self.finalizar_venta).pack(side=tk.RIGHT, padx=5)
        
        # Cargar productos iniciales
        self.buscar_productos()
        
    def buscar_productos(self):
        # Limpiar treeview
        for item in self.productos_tree.get_children():
            self.productos_tree.delete(item)
            
        # Obtener productos de la base de datos
        try:
            with next(get_db()) as db:
                producto_service = ProductoService(db)
                productos = producto_service.get_productos()
                
                for prod in productos:
                    # Aquí deberías obtener también el stock disponible
                    self.productos_tree.insert("", tk.END, values=(
                        prod.producto_id,
                        prod.nombre,
                        f"${prod.precio:,.2f}",
                        "10"  # Esto debería ser el stock real
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la lista de productos: {str(e)}")
    
    def agregar_a_venta(self):
        selected = self.productos_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para agregar")
            return
            
        producto = self.productos_tree.item(selected[0])['values']
        # Implementar lógica para agregar a la venta
        
    def quitar_de_venta(self):
        selected = self.venta_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para quitar")
            return
            
        # Implementar lógica para quitar de la venta
        
    def finalizar_venta(self):
        # Implementar lógica para finalizar la venta
        pass