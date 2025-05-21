import tkinter as tk
from tkinter import ttk, messagebox
from services.empleados_service import EmpleadoService
from persistence.db import get_db
from datetime import datetime

class EmpleadosCRUD(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Empleados")
        self.geometry("1000x650")
        
        # Variables de instancia
        self.current_empleado = None
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview para mostrar empleados
        self.tree = ttk.Treeview(main_frame, columns=(
            "ID", "Nombre", "Apellido", "Rol", "Email", "Teléfono", 
            "Contratación", "Salario"
        ), show="headings")
        
        # Configurar columnas
        columns = {
            "ID": 50,
            "Nombre": 120,
            "Apellido": 120,
            "Rol": 100,
            "Email": 150,
            "Teléfono": 100,
            "Contratación": 120,
            "Salario": 100
        }
        
        for col, width in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=tk.CENTER if col in ["ID", "Salario"] else tk.W)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Frame para formulario
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Empleado", padding=10)
        form_frame.pack(fill=tk.X, pady=10)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W)
        self.nombre_entry = ttk.Entry(form_frame)
        self.nombre_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Apellido:").grid(row=1, column=0, sticky=tk.W)
        self.apellido_entry = ttk.Entry(form_frame)
        self.apellido_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Rol:").grid(row=2, column=0, sticky=tk.W)
        self.rol_combobox = ttk.Combobox(form_frame, values=["Gerente", "Vendedor", "Almacenista"], state="readonly")
        self.rol_combobox.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Email:").grid(row=3, column=0, sticky=tk.W)
        self.email_entry = ttk.Entry(form_frame)
        self.email_entry.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Teléfono:").grid(row=4, column=0, sticky=tk.W)
        self.telefono_entry = ttk.Entry(form_frame)
        self.telefono_entry.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Fecha Contratación:").grid(row=5, column=0, sticky=tk.W)
        self.fecha_entry = ttk.Entry(form_frame)
        self.fecha_entry.grid(row=5, column=1, sticky=tk.EW, padx=5, pady=2)
        ttk.Button(form_frame, text="Hoy", command=self.set_fecha_hoy).grid(row=5, column=2, padx=5)
        
        ttk.Label(form_frame, text="Salario:").grid(row=6, column=0, sticky=tk.W)
        self.salario_entry = ttk.Entry(form_frame)
        self.salario_entry.grid(row=6, column=1, sticky=tk.EW, padx=5, pady=2)
        
        # Configurar grid del formulario
        form_frame.columnconfigure(1, weight=1)
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Nuevo", command=self.nuevo_empleado).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Guardar", command=self.guardar_empleado).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Editar", command=self.editar_empleado).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar", command=self.eliminar_empleado).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar", command=self.actualizar_lista).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cerrar", command=self.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Cargar datos iniciales
        self.actualizar_lista()
        self.limpiar_formulario()
        
    def set_fecha_hoy(self):
        self.fecha_entry.delete(0, tk.END)
        self.fecha_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
    def limpiar_formulario(self):
        self.current_empleado = None
        for entry in [self.nombre_entry, self.apellido_entry, self.email_entry, 
                     self.telefono_entry, self.fecha_entry, self.salario_entry]:
            entry.delete(0, tk.END)
        self.rol_combobox.set('')
        
    def cargar_formulario(self, empleado):
        self.current_empleado = empleado
        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, empleado.nombre)
        self.apellido_entry.delete(0, tk.END)
        self.apellido_entry.insert(0, empleado.apellido)
        self.rol_combobox.set(empleado.rol)
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, empleado.email or '')
        self.telefono_entry.delete(0, tk.END)
        self.telefono_entry.insert(0, empleado.telefono or '')
        self.fecha_entry.delete(0, tk.END)
        self.fecha_entry.insert(0, empleado.fecha_contratacion.strftime("%Y-%m-%d"))
        self.salario_entry.delete(0, tk.END)
        self.salario_entry.insert(0, str(empleado.salario))
        
    def actualizar_lista(self):
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Obtener empleados de la base de datos
        try:
            with next(get_db()) as db:
                empleado_service = EmpleadoService(db)
                empleados = empleado_service.get_empleados()
                
                for emp in empleados:
                    self.tree.insert("", tk.END, values=(
                        emp.empleado_id,
                        emp.nombre,
                        emp.apellido,
                        emp.rol,
                        emp.email,
                        emp.telefono,
                        emp.fecha_contratacion.strftime("%Y-%m-%d"),
                        f"${emp.salario:,.2f}"
                    ), tags=('readonly',))
                    
            # Configurar tags para filas
            self.tree.tag_configure('readonly', foreground='gray')
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la lista de empleados: {str(e)}")
    
    def nuevo_empleado(self):
        self.limpiar_formulario()
        self.set_fecha_hoy()
        self.nombre_entry.focus()
        
    def guardar_empleado(self):
        # Validar campos obligatorios
        if not self.nombre_entry.get() or not self.apellido_entry.get() or not self.rol_combobox.get():
            messagebox.showwarning("Validación", "Nombre, Apellido y Rol son campos obligatorios")
            return
            
        try:
            empleado_data = {
                "nombre": self.nombre_entry.get(),
                "apellido": self.apellido_entry.get(),
                "rol": self.rol_combobox.get(),
                "email": self.email_entry.get() or None,
                "telefono": self.telefono_entry.get() or None,
                "fecha_contratacion": self.fecha_entry.get(),
                "salario": float(self.salario_entry.get()) if self.salario_entry.get() else 0.0
            }
            
            with next(get_db()) as db:
                empleado_service = EmpleadoService(db)
                
                if self.current_empleado:
                    # Actualizar empleado existente
                    empleado = empleado_service.update_empleado(
                        self.current_empleado.empleado_id, 
                        empleado_data
                    )
                    messagebox.showinfo("Éxito", f"Empleado {empleado.nombre} actualizado correctamente")
                else:
                    # Crear nuevo empleado
                    empleado = empleado_service.create_empleado(empleado_data)
                    messagebox.showinfo("Éxito", f"Empleado {empleado.nombre} creado con ID: {empleado.empleado_id}")
                
                db.commit()
                self.actualizar_lista()
                self.limpiar_formulario()
                
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el empleado: {str(e)}")
        
    def editar_empleado(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para editar")
            return
            
        empleado_id = self.tree.item(selected[0])['values'][0]
        
        try:
            with next(get_db()) as db:
                empleado_service = EmpleadoService(db)
                empleado = empleado_service.get_empleado_by_id(empleado_id)
                
                if empleado:
                    self.cargar_formulario(empleado)
                else:
                    messagebox.showerror("Error", "Empleado no encontrado")
                    
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el empleado: {str(e)}")
        
    def eliminar_empleado(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para eliminar")
            return
            
        empleado_id = self.tree.item(selected[0])['values'][0]
        empleado_nombre = self.tree.item(selected[0])['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al empleado {empleado_nombre}?"):
            try:
                with next(get_db()) as db:
                    empleado_service = EmpleadoService(db)
                    empleado_service.delete_empleado(empleado_id)
                    db.commit()
                messagebox.showinfo("Éxito", "Empleado eliminado correctamente")
                self.actualizar_lista()
                self.limpiar_formulario()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el empleado: {str(e)}")



    