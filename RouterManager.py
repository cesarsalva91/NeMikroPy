from librouteros import connect
from librouteros.exceptions import TrapError
from ExcelReader import ExcelReader  # Añade esta línea al principio del archivo

class RouterManager:
    def __init__(self, router_ip, username, password, port):
        self.router_ip = router_ip
        self.username = username
        self.password = password
        self.port = port
        self.api = None
        self.connection_status = None  # Nuevo atributo para almacenar el estado de la conexión

    def connect_to_router(self):
        try:
            # Conexión al router MikroTik
            self.api = connect(username=self.username, password=self.password, host=self.router_ip, port=self.port)
            self.connection_status = "Conectado"
            return True
        except TrapError as e:
            error_message = f"Error en MikroTik API (TrapError) al conectar con {self.router_ip}:{self.port}: {e}"
            print(error_message)
            self.connection_status = error_message
        except Exception as e:
            error_message = f"Error inesperado al conectar con {self.router_ip}:{self.port}: {e}"
            print(error_message)
            self.connection_status = error_message
        return False

    def get_router_info(self):
        if not self.api:
            print("No hay conexión al router. Llame a connect_to_router() primero.")
            return None

        try:
            # Obtener información del sistema
            identity = list(self.api.path('system', 'identity'))
            system_resource = list(self.api.path('system', 'resource'))
            
            # Imprimir la información recibida para depuración
            print("Respuesta de 'system identity':", identity)
            print("Respuesta de 'system resource':", system_resource)

            # Extraer la información
            nombre = identity[0].get('name', 'Desconocido') if identity else 'Desconocido'
            modelo = system_resource[0].get('board-name', 'Desconocido') if system_resource else 'Desconocido'
            numero_serie = system_resource[0].get('serial-number', 'Desconocido') if system_resource else 'Desconocido'
            version_firmware = system_resource[0].get('version', 'Desconocido') if system_resource else 'Desconocido'
            
            return {
                'nombre': nombre,
                'modelo': modelo,
                'numero_serie': numero_serie,
                'version_firmware': version_firmware,
                'ip_router': self.router_ip,
                'connection_status': self.connection_status
            }
        except Exception as e:
            error_message = f"Error al obtener información del router: {e}"
            print(error_message)
            self.connection_status = error_message
            return None

    def run(self):
        if self.connect_to_router():
            info = self.get_router_info()
            if info:
                excel_reader = ExcelReader("Network_Devices_List.xlsx")
                excel_reader.save_router_info(info)
        return self.connection_status

# Uso de la clase
if __name__ == "__main__":
    # Parámetros de conexión
    router_ip = "192.168.240.135"  # Cambia esto por la IP de tu equipo MikroTik
    username = "admin"         # Cambia esto por tu usuario
    password = "admin"              # Cambia esto por tu contraseña
    port = 8729                # Puerto API por defecto, cambia si es necesario

    # Crear instancia y ejecutar
    router_manager = RouterManager(router_ip, username, password, port)
    connection_status = router_manager.run()
    print(f"Estado de la conexión: {connection_status}")