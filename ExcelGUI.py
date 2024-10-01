import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import font as tkfont
from ExcelReader import ExcelReader

class ExcelGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Lector de Excel")
        self.master.geometry("800x600")

        self.excel_reader = None

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
        data = self.excel_reader.read_equipment_data()
        if data:
            # Configurar columnas
            columns = list(data[0].keys())
            self.tree["columns"] = columns
            self.tree["show"] = "headings"
            for col in columns:
                self.tree.heading(col, text=col.capitalize())
                self.tree.column(col, anchor="center", width=100, minwidth=100)

            # Insertar datos
            for i, item in enumerate(data):
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
                    max(default_font.measure(str(row[col])) for row in data)
                )
                self.tree.column(col, width=min(max_width + 10, max_column_width))

            # Actualizar la vista
            self.master.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelGUI(root)
    root.mainloop()