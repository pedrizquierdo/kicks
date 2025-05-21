import tkinter as tk
from tkinter import ttk, messagebox
from services.empleados_service import EmpleadoService
from persistence.db import get_db
from interface.gerente_menu import GerenteMenu
from interface.vendedor_menu import VendedorMenu
from interface.almacenista_menu import AlmacenistaMenu

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login - Tienda Deportiva")
        self.geometry("300x200")
        self.resizable(False, False)
        
        self.configure(bg='#f0f0f0')
        
        # Frame principal
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Estilo
        style = ttk.Style()
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('TEntry', font=('Arial', 10))
        
        # Widgets
        ttk.Label(main_frame, text="Sistema de Tienda Deportiva", font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=10, columnspan=2)
        
        ttk.Label(main_frame, text="ID de Empleado:").grid(row=1, column=0, pady=5, sticky=tk.W)
        self.empleado_id_entry = ttk.Entry(main_frame)
        self.empleado_id_entry.grid(row=1, column=1, pady=5, sticky=tk.EW)
        
        login_btn = ttk.Button(main_frame, text="Ingresar", command=self.validar_login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=15, sticky=tk.EW)
        
        # Configurar grid
        main_frame.columnconfigure(1, weight=1)
        
    def validar_login(self):
        empleado_id = self.empleado_id_entry.get()
        
        if not empleado_id.isdigit():
            messagebox.showerror("Error", "El ID debe ser un número")
            return
            
        try:
            with next(get_db()) as db:
                empleado_service = EmpleadoService(db)
                empleado = empleado_service.get_empleado_by_id(int(empleado_id))
                
                if not empleado:
                    messagebox.showerror("Error", "Empleado no encontrado")
                    return
                
                # Mostrar menú según rol
                self.withdraw()  # Ocultar ventana de login
                
                if empleado.rol == 'Gerente':
                    GerenteMenu(self, empleado)
                elif empleado.rol == 'Vendedor':
                    VendedorMenu(self, empleado)
                elif empleado.rol == 'Almacenista':
                    AlmacenistaMenu(self, empleado)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al validar empleado: {str(e)}")

def run_login():
    app = LoginWindow()
    app.mainloop()