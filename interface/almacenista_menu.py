import tkinter as tk
from tkinter import ttk, messagebox
from interface.inventario_view import InventarioView

class AlmacenistaMenu(tk.Toplevel):
    def __init__(self, parent, empleado):
        super().__init__(parent)
        self.title(f"Menú Almacenista - {empleado.nombre} {empleado.apellido}")
        self.geometry("400x300")
        self.resizable(False, False)
        
        self.empleado = empleado
        
        # Frame principal
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bienvenida
        ttk.Label(
            main_frame, 
            text=f"Bienvenido, Almacenista {empleado.nombre}",
            font=('Arial', 12, 'bold')
        ).pack(pady=10)
        
        # Botones de opciones
        ttk.Button(
            main_frame, 
            text="Gestionar Inventario",
            command=self.gestionar_inventario
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            main_frame, 
            text="Registrar Entrada",
            command=self.registrar_entrada
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            main_frame, 
            text="Registrar Salida",
            command=self.registrar_salida
        ).pack(fill=tk.X, pady=5)
        
        ttk.Button(
            main_frame, 
            text="Cerrar Sesión",
            command=self.cerrar_sesion
        ).pack(fill=tk.X, pady=20)
        
    def gestionar_inventario(self):
        InventarioView(self)
        
    def registrar_entrada(self):
        messagebox.showinfo("Entrada", "Funcionalidad de registro de entrada en desarrollo")
        
    def registrar_salida(self):
        messagebox.showinfo("Salida", "Funcionalidad de registro de salida en desarrollo")
        
    def cerrar_sesion(self):
        self.destroy()
        self.master.deiconify()