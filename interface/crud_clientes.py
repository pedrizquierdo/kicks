import tkinter as tk
from tkinter import ttk, messagebox
from services.cliente_service import ClienteService  
from persistence.db import get_db
from datetime import datetime

class ClientesCRUD(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Clientes")
        self.geometry("1000x600")
        
        self.current_cliente = None
        
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tree = ttk.Treeview(main_frame, columns=(
            "ID", "Nombre", "Apellido", "Email", "Teléfono", "Dirección", 
            "Nacimiento", "Registro", "Tipo"
        ), show="headings")

        columnas = {
            "ID": 50,
            "Nombre": 100,
            "Apellido": 100,
            "Email": 150,
            "Teléfono": 100,
            "Dirección": 150,
            "Nacimiento": 100,
            "Registro": 120,
            "Tipo": 80
        }

        for col, width in columnas.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)

        self.tree.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        form_frame = ttk.LabelFrame(main_frame, text="Datos del Cliente", padding=10)
        form_frame.pack(fill=tk.X, pady=10)

        self.entries = {}
        campos = ["Nombre", "Apellido", "Email", "Teléfono", "Dirección", "Fecha Nacimiento"]
        for i, campo in enumerate(campos):
            ttk.Label(form_frame, text=campo + ":").grid(row=i, column=0, sticky=tk.W)
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, sticky=tk.EW, padx=5, pady=2)
            self.entries[campo.lower()] = entry

        ttk.Label(form_frame, text="Tipo Cliente:").grid(row=len(campos), column=0, sticky=tk.W)
        self.tipo_combobox = ttk.Combobox(form_frame, values=["Regular", "Premium"], state="readonly")
        self.tipo_combobox.grid(row=len(campos), column=1, sticky=tk.EW, padx=5, pady=2)

        form_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="Nuevo", command=self.nuevo_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Guardar", command=self.guardar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Editar", command=self.editar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar", command=self.eliminar_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar", command=self.actualizar_lista).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cerrar", command=self.destroy).pack(side=tk.RIGHT, padx=5)

        self.actualizar_lista()
        self.limpiar_formulario()

    def limpiar_formulario(self):
        self.current_cliente = None
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.tipo_combobox.set("Regular")

    def cargar_formulario(self, cliente):
        self.current_cliente = cliente
        self.entries["nombre"].insert(0, cliente.nombre)
        self.entries["apellido"].insert(0, cliente.apellido)
        self.entries["email"].insert(0, cliente.email or "")
        self.entries["teléfono"].insert(0, cliente.telefono or "")
        self.entries["dirección"].insert(0, cliente.direccion or "")
        self.entries["fecha nacimiento"].insert(0, cliente.fecha_nacimiento.strftime("%Y-%m-%d") if cliente.fecha_nacimiento else "")
        self.tipo_combobox.set(cliente.tipo_cliente)

    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            with next(get_db()) as db:
                service = ClienteService(db)
                clientes = service.get_clientes()
                for c in clientes:
                    self.tree.insert("", tk.END, values=(
                        c.cliente_id, c.nombre, c.apellido, c.email, c.telefono,
                        c.direccion, c.fecha_nacimiento.strftime("%Y-%m-%d") if c.fecha_nacimiento else '',
                        c.fecha_registro.strftime("%Y-%m-%d %H:%M") if c.fecha_registro else '',
                        c.tipo_cliente
                    ))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def nuevo_cliente(self):
        self.limpiar_formulario()
        self.entries["nombre"].focus()

    def guardar_cliente(self):
        try:
            data = {
                "nombre": self.entries["nombre"].get(),
                "apellido": self.entries["apellido"].get(),
                "email": self.entries["email"].get() or None,
                "telefono": self.entries["teléfono"].get() or None,
                "direccion": self.entries["dirección"].get() or None,
                "fecha_nacimiento": self.entries["fecha nacimiento"].get() or None,
                "tipo_cliente": self.tipo_combobox.get() or "Regular"
            }

            if not data["nombre"] or not data["apellido"]:
                messagebox.showwarning("Validación", "Nombre y Apellido son obligatorios.")
                return

            with next(get_db()) as db:
                service = ClienteService(db)
                if self.current_cliente:
                    cliente = service.update_cliente(self.current_cliente.cliente_id, data)
                    messagebox.showinfo("Éxito", f"Cliente {cliente.nombre} actualizado.")
                else:
                    cliente = service.create_cliente(data)
                    messagebox.showinfo("Éxito", f"Cliente {cliente.nombre} creado con ID {cliente.cliente_id}.")
                db.commit()
                self.actualizar_lista()
                self.limpiar_formulario()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def editar_cliente(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para editar.")
            return
        cliente_id = self.tree.item(selected[0])['values'][0]
        try:
            with next(get_db()) as db:
                service = ClienteService(db)
                cliente = service.get_cliente_by_id(cliente_id)
                if cliente:
                    self.limpiar_formulario()
                    self.cargar_formulario(cliente)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_cliente(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar.")
            return
        cliente_id = self.tree.item(selected[0])['values'][0]
        nombre = self.tree.item(selected[0])['values'][1]
        if messagebox.askyesno("Confirmar", f"¿Eliminar cliente {nombre}?"):
            try:
                with next(get_db()) as db:
                    service = ClienteService(db)
                    service.delete_cliente(cliente_id)
                    db.commit()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                self.actualizar_lista()
                self.limpiar_formulario()
            except Exception as e:
                messagebox.showerror("Error", str(e))