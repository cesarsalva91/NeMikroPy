from ExcelReader import ExcelReader
from RouterManager import RouterManager
from librouteros.exceptions import TrapError
import pandas as pd

class NewUsers:
    def __init__(self, router_manager: RouterManager, excel_file: str):
        self.router_manager = router_manager
        self.excel_reader = ExcelReader(excel_file)
        self.users_data = []

    def load_users_data(self):
        """Carga los datos de usuarios desde el archivo Excel."""
        self.users_data = self.excel_reader.read_equipment_data()

    def create_users(self):
        """Crea los usuarios en el router MikroTik."""
        if not self.router_manager.api:
            print("No hay conexión al router. Conectando...")
            if not self.router_manager.connect_to_router():
                print("No se pudo conectar al router.")
                return

        for user in self.users_data:
            username = user.get('Username')
            password = user.get('Password')
            group = user.get('Group')
            
            # Validar si el campo de grupo está vacío
            if pd.isna(group) or group == "" or group is None:
                group = 'read'  # Asignar 'read' como grupo por defecto si está vacío
            
            print(f"Procesando usuario: {username}, Grupo: {group}")

            if not username or not password:
                print(f"Datos de usuario incompletos: {user}")
                continue

            try:
                # Crear el usuario
                self.router_manager.api.path('user').add(
                    name=username,
                    password=password,
                    group=group
                )
                print(f"Usuario '{username}' creado exitosamente en el grupo '{group}'.")
            except TrapError as e:
                print(f"Error al crear el usuario '{username}': {e}")
            except Exception as e:
                print(f"Error inesperado al crear el usuario '{username}': {e}")

    def run(self):
        """Ejecuta el proceso de creación de usuarios."""
        self.load_users_data()
        self.create_users()

# Ejemplo de uso
if __name__ == "__main__":
    
    router_ip = "192.168.240.134"  # Cambia esto por la IP de tu equipo MikroTik
    username = "admin"         # Cambia esto por tu usuario
    password = "admin"              # Cambia esto por tu contraseña
    port = 4444                # Puerto API por defecto, cambia si es necesario

    excel_file = "nuevos_usuarios.xlsx"

    router_manager = RouterManager(router_ip, username, password, port)
    new_users = NewUsers(router_manager, excel_file)
    new_users.run()