import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from librouteros import connect
from librouteros.exceptions import TrapError
from NewUsers import NewUsers
from RouterManager import RouterManager


class NewUserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Usuarios")

        # Variables para almacenar los archivos
        self.equipos_file = None
        self.usuarios_file = None

        # Botón para seleccionar archivo de equipos
        self.select_equipos_button = ttk.Button(self.root, text="Seleccionar archivo de equipos", command=self.select_equipos_file)
        self.select_equipos_button.pack(pady=10)

        # Área de texto para mostrar datos de equipos
        self.equipos_text = tk.Text(self.root, height=10, width=80)
        self.equipos_text.pack(pady=10)

        # Botón para seleccionar archivo de usuarios
        self.select_usuarios_button = ttk.Button(self.root, text="Seleccionar archivo de usuarios", command=self.select_usuarios_file)
        self.select_usuarios_button.pack(pady=10)

        # Área de texto para mostrar datos de usuarios
        self.usuarios_text = tk.Text(self.root, height=10, width=80)
        self.usuarios_text.pack(pady=10)

        # Botón para cargar usuarios en los equipos
        self.load_users_button = ttk.Button(self.root, text="Cargar Usuarios en Equipos", command=self.load_users)
        self.load_users_button.pack(pady=10)

    def select_equipos_file(self):
        self.equipos_file = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        if self.equipos_file:
            self.show_equipos_data()

    def show_equipos_data(self):
        try:
            df = pd.read_excel(self.equipos_file)
            self.equipos_text.delete(1.0, tk.END)  # Limpiar el área de texto
            self.equipos_text.insert(tk.END, df.to_string(index=False))  # Mostrar datos
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo de equipos: {e}")

    def select_usuarios_file(self):
        self.usuarios_file = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        if self.usuarios_file:
            self.show_usuarios_data()

    def show_usuarios_data(self):
        try:
            df = pd.read_excel(self.usuarios_file)
            self.usuarios_text.delete(1.0, tk.END)  # Limpiar el área de texto
            self.usuarios_text.insert(tk.END, df.to_string(index=False))  # Mostrar datos
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo de usuarios: {e}")

    def load_users(self):
        if not self.equipos_file or not self.usuarios_file:
            messagebox.showerror("Error", "Por favor, seleccione ambos archivos.")
            return

        try:
            # Leer archivos
            equipos_df = pd.read_excel(self.equipos_file)
            usuarios_df = pd.read_excel(self.usuarios_file)

            # Verificar que los archivos tengan las columnas correctas
            required_equipos_columns = ['IP', 'Usuario', 'Pass', 'Puerto API', 'Nombre del Equipo']
            required_usuarios_columns = ['Username', 'Password', 'Group']
            
            

            for col in required_equipos_columns:
                if col not in equipos_df.columns:
                    messagebox.showerror("Error", f"El archivo de equipos debe contener la columna '{col}'.")
                    return

            for col in required_usuarios_columns:
                if col not in usuarios_df.columns:
                    messagebox.showerror("Error", f"El archivo de usuarios debe contener la columna '{col}'.")
                    return

            # Procesar cada equipo
            for _, equipo_row in equipos_df.iterrows():
                ip = equipo_row['IP']
                username = equipo_row['Usuario']
                password = equipo_row['Pass']
                port = equipo_row['Puerto API']
                nombre_equipo = equipo_row['Nombre del Equipo']

                # Crear instancia de RouterManager y conectar
                router_manager = RouterManager(ip, username, password, port)
                
                
                if router_manager.connect_to_router():
                    # Procesar usuarios para cada equipo
                    for _, user_row in usuarios_df.iterrows():
                       
                        # Crear el usuario en el router
                        print("***************llegue hasta aqui ************************")
                        new_users = NewUsers(router_manager, self.usuarios_file)
                        new_users.run()
                        
                        #if router_manager.create_user(user_to_add, user_password):
                        #    print(f"Usuario '{user_to_add}' creado en {nombre_equipo} ({ip}) con grupo '{user_group}'.")
                        #else:
                        #    print(f"Error al crear el usuario '{user_to_add}' en {nombre_equipo} ({ip}).")
                else:
                    print(f"No se pudo conectar a {nombre_equipo} ({ip}).")

            messagebox.showinfo("Éxito", "Usuarios cargados en los equipos.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar usuarios: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NewUserGUI(root)
    root.mainloop()
