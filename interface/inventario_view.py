import tkinter as tk
from tkinter import ttk, messagebox
from services.inventario_service import InventarioService
from services.producto_service import ProductoService
from persistence.db import get_db

class InventarioView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Inventario")
        self.geometry("900x600")
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de filtros
        filter_frame = ttk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Filtrar por:").pack(side=tk.LEFT)
        
        self.filter_var = tk.StringVar()
        filter_options = ["Todos", "Bajo stock", "Por producto", "Por ubicación"]
        self.filter_cb = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=filter_options, state="readonly")
        self.filter_cb.pack(side=tk.LEFT, padx=5)
        self.filter_cb.current(0)
        
        ttk.Button(filter_frame, text="Aplicar", command=self.aplicar_filtro).pack(side=tk.LEFT)
        
        # Treeview para inventario
        self.tree = ttk.Treeview(main_frame, columns=(
            "ID", "Producto", "Talla", "Color", "Cantidad", "Ubicación", 
            "Última Entrada", "Última Salida"
        ), show="headings")
        
        columns = {
            "ID": 50,
            "Producto": 150,
            "Talla": 60,
            "Color": 80,
            "Cantidad": 70,
            "Ubicación": 100,
            "Última Entrada": 120,
            "Última Salida": 120
        }
        
        for col, width in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=tk.CENTER if col in ["ID", "Talla", "Cantidad"] else tk.W)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Agregar Stock", command=self.agregar_stock).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Ajustar Stock", command=self.ajustar_stock).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar", command=self.actualizar_lista).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cerrar", command=self.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Cargar datos iniciales
        self.actualizar_lista()
        
    def actualizar_lista(self):
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Obtener inventario de la base de datos
        try:
            with next(get_db()) as db:
                inventario_service = InventarioService(db)
                producto_service = ProductoService(db)
                
                items = inventario_service.get_inventario()
                
                for item in items:
                    producto = producto_service.get_producto(item.producto_id)
                    self.tree.insert("", tk.END, values=(
                        item.inventario_id,
                        producto.nombre if producto else "N/A",
                        item.talla,
                        item.color,
                        item.cantidad_disponible,
                        item.ubicacion_almacen,
                        item.fecha_ultima_entrada.strftime("%Y-%m-%d %H:%M") if item.fecha_ultima_entrada else "N/A",
                        item.fecha_ultima_salida.strftime("%Y-%m-%d %H:%M") if item.fecha_ultima_salida else "N/A"
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el inventario: {str(e)}")
    
    def aplicar_filtro(self):
        filtro = self.filter_var.get()
        # Implementar lógica de filtrado
        messagebox.showinfo("Filtro", f"Filtrando por: {filtro}")
        
    def agregar_stock(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un item del inventario")
            return
            
        # Implementar lógica para agregar stock
        messagebox.showinfo("Agregar", "Funcionalidad para agregar stock en desarrollo")
        
    def ajustar_stock(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un item del inventario")
            return
            
        # Implementar lógica para ajustar stock
        messagebox.showinfo("Ajustar", "Funcionalidad para ajustar stock en desarrollo")