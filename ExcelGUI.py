import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from tkinter import font as tkfont
from ExcelReader import ExcelReader
from RouterManager import RouterManager

class ExcelGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Lector de Excel")
        self.master.geometry("800x600")

        self.excel_reader = None
        self.equipment_data = None

        # Estilo para el Treeview
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#E1E1E1", 
                             fieldbackground="#E1E1E1", foreground="black")
        self.style.map('Treeview', background=[('selected', '#3366CC')])
        self.style.configure("Treeview.Heading", font=('Calibri', 13, 'bold'))

        # Frame principal
        self.main_frame = ttk.Frame(master, padding="3 3 12 12")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Botón para seleccionar archivo
        self.select_button = ttk.Button(self.main_frame, text="Seleccionar archivo Excel", 
                                        command=self.select_file)
        self.select_button.pack(pady=10)

        # Botón para obtener información de los equipos
        self.get_info_button = ttk.Button(self.main_frame, text="Obtener información de equipos", 
                                          command=self.get_equipment_info, state=tk.DISABLED)
        self.get_info_button.pack(pady=10)

        # Frame para el Treeview (inicialmente vacío)
        self.tree_frame = None
        self.tree = None
        self.scrollbar = None
        self.x_scrollbar = None

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if file_path:
            self.excel_reader = ExcelReader(file_path)
            self.load_data()

    def load_data(self):
        # Limpiar datos anteriores si existen
        if self.tree_frame:
            self.tree_frame.destroy()

        # Crear nuevo frame para el Treeview
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        # Crear nuevo Treeview con scrollbars
        self.tree = ttk.Treeview(self.tree_frame, style="Treeview")
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.x_scrollbar = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)

        # Configurar el Treeview para usar los scrollbars
        self.tree.configure(yscrollcommand=self.scrollbar.set, xscrollcommand=self.x_scrollbar.set)

        # Posicionar el Treeview y los scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.x_scrollbar.grid(row=1, column=0, sticky='ew')

        # Configurar el grid para que el Treeview se expanda
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        # Cargar nuevos datos
        self.equipment_data = self.excel_reader.read_equipment_data()
        
        if self.equipment_data:
            # Configurar columnas
            columns = list(self.equipment_data[0].keys())
            self.tree["columns"] = columns
            self.tree["show"] = "headings"
            for col in columns:
                self.tree.heading(col, text=col.capitalize())
                self.tree.column(col, anchor="center", width=100, minwidth=100)

            # Insertar datos
            for i, item in enumerate(self.equipment_data):
                tags = ('oddrow',) if i % 2 else ('evenrow',)
                self.tree.insert("", "end", values=list(item.values()), tags=tags)

            # Configurar colores alternados para las filas
            self.tree.tag_configure('oddrow', background='#E8E8E8')
            self.tree.tag_configure('evenrow', background='#DFDFDF')

            # Ajustar ancho de columnas
            max_column_width = 300  # Ajusta este valor según tus necesidades
            default_font = tkfont.nametofont("TkDefaultFont")
            for col in columns:
                max_width = max(
                    default_font.measure(str(col)),
                    max(default_font.measure(str(row[col])) for row in self.equipment_data)
                )
                self.tree.column(col, width=min(max_width + 10, max_column_width))

            # Actualizar la vista
            self.master.update_idletasks()

            # Habilitar el botón de obtener información
            self.get_info_button['state'] = tk.NORMAL

    def get_equipment_info(self):
        if not self.equipment_data:
            messagebox.showerror("Error", "No hay datos de equipos cargados.")
            return

        successful_connections = 0
        failed_connections = 0
        skipped_equipments = 0

        for equipment in self.equipment_data:
            ip = equipment.get('IP', '')
            user = equipment.get('Usuario', '')
            passU = equipment.get('Password', '')
            if not ip:
                print(f"Advertencia: El equipo {equipment.get('Nombre', 'Desconocido')} no tiene IP.")
                skipped_equipments += 1
                continue

            api_port = equipment.get('Puerto API', '')
            if not api_port:
                print(f"Advertencia: El equipo {equipment.get('Nombre', 'Desconocido')} no tiene Puerto API especificado.")
                skipped_equipments += 1
                continue

            try:
                api_port = int(api_port)
            except ValueError:
                print(f"Error: Puerto API inválido para el equipo {equipment.get('Nombre', 'Desconocido')}: {api_port}")
                skipped_equipments += 1
                continue

            print("****************************************")
            router_manager = RouterManager(router_ip=ip, username=user, password=passU, port=api_port)
            print(router_manager.get_router_info())
            connection_status = router_manager.run()

            if connection_status == "Conectado":
                successful_connections += 1
            else:
                failed_connections += 1
                print(f"Error: No se pudo conectar al equipo {equipment.get('Nombre', 'Desconocido')} con IP {ip}. Estado: {connection_status}")

        # Mostrar un resumen al final del proceso
        summary = f"Proceso completado:\n\n" \
                  f"Equipos conectados exitosamente: {successful_connections}\n" \
                  f"Equipos con fallos de conexión: {failed_connections}\n" \
                  f"Equipos omitidos: {skipped_equipments}\n\n" \
                  f"Total de equipos procesados: {len(self.equipment_data)}"
        
        messagebox.showinfo("Resumen del proceso", summary)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelGUI(root)
    root.mainloop()
