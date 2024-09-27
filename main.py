from RouterManager import RouterManager
from ExcelReader import ExcelReader

class Main:
    def __init__(self):
        self.excel_reader = ExcelReader("equipos.xlsx")  # Asegúrate de que este archivo exista
        self.router_managers = []

    def run(self):
        # Leer datos de los equipos desde Excel
        equipment_data = self.excel_reader.read_equipment_data()

        # Crear y ejecutar RouterManager para cada equipo
        for equipment in equipment_data:
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

if __name__ == "__main__":
    main = Main()
    main.run()
