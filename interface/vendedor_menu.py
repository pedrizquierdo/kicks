import tkinter as tk
from tkinter import ttk, messagebox
from interface.ventas_view import VentasView

class VendedorMenu(tk.Toplevel):
    def __init__(self, parent, empleado):
        super().__init__(parent)
        self.title(f"Menú Vendedor - {empleado.nombre} {empleado.apellido}")
        self.geometry("400x300")
        self.resizable(False, False)
        
        self.empleado = empleado
        
        # Frame principal
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bienvenida
        ttk.Label(
            main_frame, 
            text=f"Bienvenido, Vendedor {empleado.nombre}",
            font=('Arial', 12, 'bold')
        ).pack(pady=10)
        
        # Botones de opciones
        ttk.Button(
            main_frame, 
            text="Registrar Venta",
            command=self.registrar_venta
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            main_frame, 
            text="Consultar Productos",
            command=self.consultar_productos
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            main_frame, 
            text="Clientes",
            command=self.gestionar_clientes
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            main_frame, 
            text="Cerrar Sesión",
            command=self.cerrar_sesion
        ).pack(fill=tk.X, pady=20)
        
    def registrar_venta(self):
        VentasView(self, self.empleado)
        
    def consultar_productos(self):
        messagebox.showinfo("Productos", "Funcionalidad de consulta de productos en desarrollo")
        
    def gestionar_clientes(self):
        messagebox.showinfo("Clientes", "Funcionalidad de gestión de clientes en desarrollo")
        
    def cerrar_sesion(self):
        self.destroy()
        self.master.deiconify()