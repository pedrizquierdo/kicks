import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from services.inventario_service import InventarioService
from services.producto_service import ProductoService
from services.proveedor_service import ProveedorService
from persistence.db import get_db
from datetime import datetime

class RegistrarEntradaView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registrar Entrada")
        self.geometry("400x300")
        self.transient(parent)
        self.grab_set()

        # Variables
        self.producto_var = tk.IntVar()
        self.proveedor_var = tk.IntVar()
        self.cantidad_var = tk.IntVar()

        # Formulario
        ttk.Label(self, text="ID del Producto:").pack(pady=5)
        ttk.Entry(self, textvariable=self.producto_var).pack()

        ttk.Label(self, text="ID del Proveedor:").pack(pady=5)
        ttk.Entry(self, textvariable=self.proveedor_var).pack()

        ttk.Label(self, text="Cantidad a ingresar:").pack(pady=5)
        ttk.Entry(self, textvariable=self.cantidad_var).pack()

        ttk.Button(self, text="Registrar Entrada", command=self.registrar_entrada).pack(pady=15)

    def registrar_entrada(self):
        producto_id = self.producto_var.get()
        proveedor_id = self.proveedor_var.get()
        cantidad = self.cantidad_var.get()

        if producto_id <= 0 or proveedor_id <= 0 or cantidad <= 0:
            messagebox.showerror("Error", "Todos los campos deben ser válidos y mayores a 0.")
            return

        try:
            with next(get_db()) as db:
                inventario_service = InventarioService(db)
                producto_service = ProductoService(db)
                proveedor_service = ProveedorService(db)

                inventario_items = inventario_service.obtener_inventario_por_producto(producto_id)
                if not inventario_items:
                    messagebox.showerror("Error", "No se encontró inventario para ese producto.")
                    return

                inventario_id = inventario_items[0].inventario_id
                inventario_service.agregar_stock(inventario_id, cantidad)

                producto = producto_service.get_producto_by_id(producto_id)
                proveedor = proveedor_service.get_proveedor_by_id(proveedor_id)

                nombre_producto = producto.nombre if producto else "Producto desconocido"
                nombre_proveedor = proveedor.nombre if proveedor else "Proveedor desconocido"

                self.mostrar_ticket(nombre_producto, nombre_proveedor, cantidad)


        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la entrada: {str(e)}")

    def mostrar_ticket(self, producto, proveedor, cantidad):
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        contenido = (
            f"========== TICKET DE ENTRADA ==========\n"
            f"Fecha: {ahora}\n"
            f"Producto: {producto}\n"
            f"Cantidad: {cantidad}\n"
            f"Proveedor: {proveedor}\n"
            f"========================================"
        )

        ventana_ticket = tk.Toplevel(self)
        ventana_ticket.title("Ticket de Entrada")
        ventana_ticket.geometry("400x250")
        ventana_ticket.transient(self)
        ventana_ticket.grab_set()

        ttk.Label(ventana_ticket, text="Ticket de Entrada", font=("Arial", 12, "bold")).pack(pady=5)
        texto = ScrolledText(ventana_ticket, wrap=tk.WORD, width=40, height=10)
        texto.pack(padx=10, pady=5)
        texto.insert(tk.END, contenido)
        texto.config(state="disabled")

        ttk.Button(ventana_ticket, text="Cerrar", command=ventana_ticket.destroy).pack(pady=5)

        # Guardar ticket como .txt
        with open("ticket_entrada.txt", "w", encoding="utf-8") as f:
            f.write(contenido)
