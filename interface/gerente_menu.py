import tkinter as tk
from tkinter import ttk, messagebox
from interface.crud_empleados import EmpleadosCRUD
from interface.crud_productos import ProductosCRUD

class GerenteMenu(tk.Toplevel):
    def __init__(self, parent, empleado):
        super().__init__(parent)
        self.title(f"Menú Gerente - {empleado.nombre} {empleado.apellido}")
        self.geometry("400x400")
        self.resizable(False, False)
        
        self.empleado = empleado
        
        # Frame principal
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bienvenida
        ttk.Label(
            main_frame, 
            text=f"Bienvenido, Gerente {empleado.nombre}",
            font=('Arial', 12, 'bold')
        ).pack(pady=10)
        
        # Botones de opciones
        ttk.Button(
            main_frame, 
            text="Gestionar Empleados",
            command=self.abrir_crud_empleados
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            main_frame, 
            text="Gestionar Productos",
            command=self.abrir_crud_productos
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            main_frame, 
            text="Reportes",
            command=self.mostrar_reportes
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            main_frame, 
            text="Cerrar Sesión",
            command=self.cerrar_sesion
        ).pack(fill=tk.X, pady=20)
        
    def abrir_crud_empleados(self):
        EmpleadosCRUD(self)
        
    def abrir_crud_productos(self):
        ProductosCRUD(self)
        
    def mostrar_reportes(self):
        messagebox.showinfo("Reportes", "Funcionalidad de reportes en desarrollo")
        
    def cerrar_sesion(self):
        self.destroy()
        self.master.deiconify()  # Mostrar ventana de login