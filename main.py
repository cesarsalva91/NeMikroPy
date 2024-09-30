import tkinter as tk
from tkinter import filedialog, ttk
from RouterManager import RouterManager
from ExcelReader import ExcelReader

class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gestor de Routers")
        self.root.geometry("600x400")

        self.excel_reader = None
        self.router_managers = []
        self.equipment_data = []

        self.create_widgets()

    def create_widgets(self):
        # Botón para seleccionar archivo
        self.select_file_button = tk.Button(self.root, text="Seleccionar archivo de equipos", command=self.select_file)
        self.select_file_button.pack(pady=10)

        # Treeview para mostrar equipos
        self.tree = ttk.Treeview(self.root, columns=('IP', 'Puerto API', 'Nombre'), show='headings')
        self.tree.heading('IP', text='IP')
        self.tree.heading('Puerto API', text='Puerto API')
        self.tree.heading('Nombre', text='Nombre del Equipo')
        self.tree.pack(pady=10, padx=10, expand=True, fill='both')

        # Botón para procesar equipos
        self.process_button = tk.Button(self.root, text="Procesar Equipos", command=self.process_equipment, state='disabled')
        self.process_button.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.excel_reader = ExcelReader(file_path)
            self.equipment_data = self.excel_reader.read_equipment_data()
            self.update_treeview()
            self.process_button['state'] = 'normal'

    def update_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for equipment in self.equipment_data:
            self.tree.insert('', 'end', values=(equipment['IP'], equipment['Puerto API'], equipment['Nombre del Equipo']))

    def process_equipment(self):
        for equipment in self.equipment_data:
            router_ip = equipment['IP']
            username = equipment['Usuario']
            password = equipment['Contraseña']
            port = int(equipment['Puerto API'])
            name = equipment['Nombre del Equipo']

            print(f"\nProcesando equipo: {name}")
            router_manager = RouterManager(router_ip, username, password, port)
            self.router_managers.append(router_manager)
            
            try:
                router_manager.run()
            except Exception as e:
                print(f"Error al procesar el equipo {name}: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    main = Main()
    main.run()
