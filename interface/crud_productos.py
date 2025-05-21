import tkinter as tk
from tkinter import ttk, messagebox
from services.producto_service import ProductoService
from services.marcas_service import MarcaService
from services.categorias_service import CategoriaService
from persistence.db import get_db

class ProductosCRUD(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Productos")
        self.geometry("1200x700")
        
        # Variables de instancia
        self.current_producto = None
        self.marcas = []
        self.categorias = []
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview para mostrar productos
        self.tree = ttk.Treeview(main_frame, columns=(
            "ID", "Nombre", "Descripción", "Precio", "Costo", "Marca", 
            "Categoría", "Género", "Temporada", "Estado"
        ), show="headings")
        
        # Configurar columnas
        columns = {
            "ID": 50,
            "Nombre": 150,
            "Descripción": 200,
            "Precio": 80,
            "Costo": 80,
            "Marca": 100,
            "Categoría": 100,
            "Género": 80,
            "Temporada": 100,
            "Estado": 80
        }
        
        for col, width in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=tk.CENTER if col in ["ID", "Precio", "Costo", "Estado"] else tk.W)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Frame para formulario
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Producto", padding=10)
        form_frame.pack(fill=tk.X, pady=10)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W)
        self.nombre_entry = ttk.Entry(form_frame)
        self.nombre_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Descripción:").grid(row=1, column=0, sticky=tk.W)
        self.descripcion_entry = ttk.Entry(form_frame)
        self.descripcion_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Precio:").grid(row=2, column=0, sticky=tk.W)
        self.precio_entry = ttk.Entry(form_frame)
        self.precio_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Costo:").grid(row=3, column=0, sticky=tk.W)
        self.costo_entry = ttk.Entry(form_frame)
        self.costo_entry.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Marca:").grid(row=4, column=0, sticky=tk.W)
        self.marca_combobox = ttk.Combobox(form_frame, state="readonly")
        self.marca_combobox.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Categoría:").grid(row=5, column=0, sticky=tk.W)
        self.categoria_combobox = ttk.Combobox(form_frame, state="readonly")
        self.categoria_combobox.grid(row=5, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Género:").grid(row=6, column=0, sticky=tk.W)
        self.genero_combobox = ttk.Combobox(form_frame, 
            values=["Hombre", "Mujer", "Unisex", "Niño", "Niña"], 
            state="readonly")
        self.genero_combobox.grid(row=6, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Temporada:").grid(row=7, column=0, sticky=tk.W)
        self.temporada_combobox = ttk.Combobox(form_frame, 
            values=["Verano", "Invierno", "Primavera", "Otoño", "All Season"], 
            state="readonly")
        self.temporada_combobox.grid(row=7, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Estado:").grid(row=8, column=0, sticky=tk.W)
        self.estado_combobox = ttk.Combobox(form_frame, 
            values=["Activo", "Inactivo"], 
            state="readonly")
        self.estado_combobox.grid(row=8, column=1, sticky=tk.EW, padx=5, pady=2)
        self.estado_combobox.set("Activo")
        
        # Configurar grid del formulario
        form_frame.columnconfigure(1, weight=1)
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Nuevo", command=self.nuevo_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Guardar", command=self.guardar_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Editar", command=self.editar_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar", command=self.eliminar_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar", command=self.actualizar_lista).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cerrar", command=self.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Cargar datos iniciales
        self.cargar_marcas_categorias()
        self.actualizar_lista()
        self.limpiar_formulario()
        
    def cargar_marcas_categorias(self):
        try:
            with next(get_db()) as db:
                # Cargar marcas
                marca_service = MarcaService(db)
                self.marcas = marca_service.get_marcas()
                self.marca_combobox['values'] = [m.nombre for m in self.marcas]
                
                # Cargar categorías
                categoria_service = CategoriaService(db)
                self.categorias = categoria_service.get_categorias()
                self.categoria_combobox['values'] = [c.nombre for c in self.categorias]
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar marcas y categorías: {str(e)}")
        
    def limpiar_formulario(self):
        self.current_producto = None
        for entry in [self.nombre_entry, self.descripcion_entry, 
                     self.precio_entry, self.costo_entry]:
            entry.delete(0, tk.END)
        for cb in [self.marca_combobox, self.categoria_combobox, 
                  self.genero_combobox, self.temporada_combobox]:
            cb.set('')
        self.estado_combobox.set("Activo")
        
    def cargar_formulario(self, producto):
        self.current_producto = producto
        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, producto.nombre)
        self.descripcion_entry.delete(0, tk.END)
        self.descripcion_entry.insert(0, producto.descripcion or '')
        self.precio_entry.delete(0, tk.END)
        self.precio_entry.insert(0, str(producto.precio))
        self.costo_entry.delete(0, tk.END)
        self.costo_entry.insert(0, str(producto.costo))
        
        # Seleccionar marca
        if producto.marca_id:
            marca = next((m for m in self.marcas if m.marca_id == producto.marca_id), None)
            if marca:
                self.marca_combobox.set(marca.nombre)
        
        # Seleccionar categoría
        if producto.categoria_id:
            categoria = next((c for c in self.categorias if c.categoria_id == producto.categoria_id), None)
            if categoria:
                self.categoria_combobox.set(categoria.nombre)
        
        self.genero_combobox.set(producto.genero)
        self.temporada_combobox.set(producto.temporada)
        self.estado_combobox.set(producto.estado)
        
    def actualizar_lista(self):
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Obtener productos de la base de datos
        try:
            with next(get_db()) as db:
                producto_service = ProductoService(db)
                productos = producto_service.get_productos()
                
                for prod in productos:
                    marca_nombre = next((m.nombre for m in self.marcas if m.marca_id == prod.marca_id), "N/A")
                    categoria_nombre = next((c.nombre for c in self.categorias if c.categoria_id == prod.categoria_id), "N/A")
                    
                    self.tree.insert("", tk.END, values=(
                        prod.producto_id,
                        prod.nombre,
                        prod.descripcion[:50] + "..." if prod.descripcion and len(prod.descripcion) > 50 else prod.descripcion,
                        f"${prod.precio:,.2f}",
                        f"${prod.costo:,.2f}",
                        marca_nombre,
                        categoria_nombre,
                        prod.genero,
                        prod.temporada,
                        prod.estado
                    ), tags=('readonly',))
                    
            # Configurar tags para filas
            self.tree.tag_configure('readonly', foreground='gray')
            self.tree.tag_configure('inactivo', foreground='red')
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la lista de productos: {str(e)}")
    
    def nuevo_producto(self):
        self.limpiar_formulario()
        self.nombre_entry.focus()
        
    def guardar_producto(self):
        # Validar campos obligatorios
        if not self.nombre_entry.get() or not self.precio_entry.get() or not self.costo_entry.get():
            messagebox.showwarning("Validación", "Nombre, Precio y Costo son campos obligatorios")
            return
            
        if not self.marca_combobox.get() or not self.categoria_combobox.get():
            messagebox.showwarning("Validación", "Debe seleccionar una marca y una categoría")
            return
            
        try:
            # Obtener IDs de marca y categoría
            marca_nombre = self.marca_combobox.get()
            marca_id = next(m.marca_id for m in self.marcas if m.nombre == marca_nombre)
            
            categoria_nombre = self.categoria_combobox.get()
            categoria_id = next(c.categoria_id for c in self.categorias if c.nombre == categoria_nombre)
            
            producto_data = {
                "nombre": self.nombre_entry.get(),
                "descripcion": self.descripcion_entry.get() or None,
                "precio": float(self.precio_entry.get()),
                "costo": float(self.costo_entry.get()),
                "marca_id": marca_id,
                "categoria_id": categoria_id,
                "genero": self.genero_combobox.get(),
                "temporada": self.temporada_combobox.get(),
                "estado": self.estado_combobox.get()
            }
            
            with next(get_db()) as db:
                producto_service = ProductoService(db)
                
                if self.current_producto:
                    # Actualizar producto existente
                    producto = producto_service.update_producto(
                        self.current_producto.producto_id, 
                        producto_data
                    )
                    messagebox.showinfo("Éxito", f"Producto {producto.nombre} actualizado correctamente")
                else:
                    # Crear nuevo producto
                    producto = producto_service.create_producto(producto_data)
                    messagebox.showinfo("Éxito", f"Producto {producto.nombre} creado con ID: {producto.producto_id}")
                
                db.commit()
                self.actualizar_lista()
                self.limpiar_formulario()
                
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el producto: {str(e)}")
        
    def editar_producto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para editar")
            return
            
        producto_id = self.tree.item(selected[0])['values'][0]
        
        try:
            with next(get_db()) as db:
                producto_service = ProductoService(db)
                producto = producto_service.get_producto_by_id(producto_id)
                
                if producto:
                    self.cargar_formulario(producto)
                else:
                    messagebox.showerror("Error", "Producto no encontrado")
                    
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el producto: {str(e)}")
        
    def eliminar_producto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            return
            
        producto_id = self.tree.item(selected[0])['values'][0]
        producto_nombre = self.tree.item(selected[0])['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el producto {producto_nombre}?"):
            try:
                with next(get_db()) as db:
                    producto_service = ProductoService(db)
                    producto_service.delete_producto(producto_id)
                    db.commit()
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                self.actualizar_lista()
                self.limpiar_formulario()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el producto: {str(e)}")


           