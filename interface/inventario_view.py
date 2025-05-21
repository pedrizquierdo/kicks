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
                
                items = inventario_service.obtener_todo_el_inventario()

                
                for item in items:
                    producto = producto_service.get_producto_by_id(item.producto_id)

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

        item_values = self.tree.item(selected[0])["values"]
        inventario_id = item_values[0]
        producto_nombre = item_values[1]

        # Crear ventana emergente
        ventana = tk.Toplevel(self)
        ventana.title("Agregar Stock")
        ventana.geometry("300x250")
        ventana.transient(self)
        ventana.grab_set()

        # Título producto
        ttk.Label(ventana, text=f"Producto: {producto_nombre}").pack(pady=5)

        # Campo proveedor
        ttk.Label(ventana, text="ID del proveedor:").pack()
        proveedor_var = tk.IntVar()
        ttk.Entry(ventana, textvariable=proveedor_var).pack()

        # Campo cantidad
        ttk.Label(ventana, text="Cantidad a agregar:").pack()
        cantidad_var = tk.IntVar()
        ttk.Entry(ventana, textvariable=cantidad_var).pack()

        def confirmar():
            proveedor_id = proveedor_var.get()
            cantidad = cantidad_var.get()

            if proveedor_id <= 0 or cantidad <= 0:
                messagebox.showerror("Error", "Todos los campos deben ser mayores a 0")
                return

            try:
                with next(get_db()) as db:
                    inventario_service = InventarioService(db)

                    # Actualizar el inventario
                    inventario_service.agregar_stock(inventario_id, cantidad)

                    # Aquí podrías guardar una entrada en una tabla de historial si la tienes

                messagebox.showinfo("Éxito", "Stock agregado correctamente")
                self.actualizar_lista()
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar stock: {str(e)}")

        ttk.Button(ventana, text="Confirmar", command=confirmar).pack(pady=10)


        
    def ajustar_stock(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un item del inventario")
            return

        item_values = self.tree.item(selected[0])["values"]
        inventario_id = item_values[0]
        producto_nombre = item_values[1]
        stock_actual = item_values[4]

        ventana = tk.Toplevel(self)
        ventana.title("Ajustar Stock")
        ventana.geometry("300x200")
        ventana.transient(self)
        ventana.grab_set()

        ttk.Label(ventana, text=f"Producto: {producto_nombre}").pack(pady=5)
        ttk.Label(ventana, text=f"Stock actual: {stock_actual}").pack(pady=5)

        nueva_cantidad_var = tk.IntVar()
        ttk.Label(ventana, text="Nuevo stock real:").pack()
        ttk.Entry(ventana, textvariable=nueva_cantidad_var).pack()

        def confirmar_ajuste():
            nueva_cantidad = nueva_cantidad_var.get()
            if nueva_cantidad < 0:
                messagebox.showerror("Error", "El stock no puede ser negativo.")
                return

            try:
                with next(get_db()) as db:
                    inventario_service = InventarioService(db)
                    inventario_service.actualizar_elemento_inventario(
                        inventario_id=inventario_id,
                        cantidad=nueva_cantidad
                    )

                messagebox.showinfo("Éxito", "Stock ajustado correctamente.")
                self.actualizar_lista()
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo ajustar el stock: {str(e)}")

        ttk.Button(ventana, text="Confirmar", command=confirmar_ajuste).pack(pady=10)
