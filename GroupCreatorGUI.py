import tkinter as tk
from tkinter import ttk, messagebox
from NewGroup import NewGroup
from RouterManager import RouterManager

class GroupCreatorGUI:
    def __init__(self, router_manager):
        self.router_manager = router_manager
        self.new_group = NewGroup(router_manager)

        self.root = tk.Tk()
        self.root.title("Creador de Grupos")
        self.root.geometry("400x600")

        self.create_widgets()

    def create_widgets(self):
        # Campo para el nombre del grupo
        ttk.Label(self.root, text="Nombre del Grupo:").grid(row=0, column=0, pady=5)
        self.group_name_entry = ttk.Entry(self.root)
        self.group_name_entry.grid(row=0, column=1, pady=5)

        # Campo para el skin del grupo
        ttk.Label(self.root, text="Skin del Grupo:").grid(row=1, column=0, pady=5)
        self.skin_entry = ttk.Entry(self.root)  # Nuevo campo de texto para el skin
        self.skin_entry.grid(row=1, column=1, pady=5)

        # Checkboxes para los atributos
        ttk.Label(self.root, text="Atributos:").grid(row=2, column=0, pady=5, columnspan=2)
        self.attributes = [
            "read", "write", "test", "web", "local", "telnet", "ssh", "ftp",
            "reboot", "policy", "winbox", "password", "sniff", "sensitive",
            "api", "romon", "dude", "tikapp"
        ]
        self.checkboxes = {}
        for index, attr in enumerate(self.attributes):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(self.root, text=attr, variable=var)
            # Distribuir en dos columnas
            cb.grid(row=(index // 2) + 3, column=index % 2, sticky='w', padx=20)
            self.checkboxes[attr] = var

        # Botón para crear el grupo
        ttk.Button(self.root, text="Crear Grupo", command=self.create_group).grid(row=len(self.attributes) // 2 + 3, columnspan=2, pady=20)

    def create_group(self):
        group_name = self.group_name_entry.get()
        skin = self.skin_entry.get()  # Obtener el skin del nuevo campo de texto
        if not group_name:
            messagebox.showerror("Error", "Por favor, ingrese un nombre para el grupo.")
            return

        self.new_group.set_group_name(group_name)
        self.new_group.set_attribute("skin", skin)  # Establecer el skin

        # Recopilar atributos seleccionados
        selected_attributes = [attr for attr, var in self.checkboxes.items() if var.get()]
        policy = ",".join(selected_attributes)
        self.new_group.set_attribute("policy", policy)

        # Intentar crear el grupo
        if self.new_group.run():
            messagebox.showinfo("Éxito", f"Grupo '{group_name}' creado exitosamente.")
            self.group_name_entry.delete(0, tk.END)  # Limpiar el campo de nombre
            self.skin_entry.delete(0, tk.END)  # Limpiar el campo de skin
            for var in self.checkboxes.values():
                var.set(False)  # Desmarcar todos los checkboxes
        else:
            messagebox.showerror("Error", f"No se pudo crear el grupo '{group_name}'.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    router_ip = "192.168.240.134"
    username = "admin"
    password = "admin"
    port = 4444

    router_manager = RouterManager("192.168.240.135", "admin", "admin", "8728")
    app = GroupCreatorGUI(router_manager)
    app.run()
