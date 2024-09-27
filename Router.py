from librouteros import connect
from librouteros.exceptions import TrapError

class RouterManager:
    def __init__(self, router_ip, username, password, port):
        self.router_ip = router_ip
        self.username = username
        self.password = password
        self.port = port
        self.api = None

    def connect_to_router(self):
        try:
            # Conexión al router MikroTik
            self.api = connect(username=self.username, password=self.password, host=self.router_ip, port=self.port)
            return True
        except TrapError as e:
            print(f"Error en MikroTik API (TrapError) al conectar con {self.router_ip}:{self.port}: {e}")
        except Exception as e:
            print(f"Error inesperado al conectar con {self.router_ip}:{self.port}: {e}")
        return False

    def get_router_info(self):
        if not self.api:
            print("No hay conexión al router. Llame a connect_to_router() primero.")
            return None

        try:
            # Obtener información del sistema
            identity = self.api.path('system', 'identity')
            system_resource = self.api.path('system', 'resource')
            
            # Imprimir la información recibida para depuración
            print("Respuesta de 'system identity':", list(identity))
            print("Respuesta de 'system resource':", list(system_resource))

            # Extraer la información
            nombre = next(identity).get('name', 'Desconocido')
            resource = next(system_resource)
            modelo = resource.get('board-name', 'Desconocido')
            numero_serie = resource.get('serial-number', 'Desconocido')
            version_firmware = resource.get('version', 'Desconocido')
            
            return {
                'nombre': nombre,
                'modelo': modelo,
                'numero_serie': numero_serie,
                'version_firmware': version_firmware,
                'ip_router': self.router_ip
            }
        except Exception as e:
            print(f"Error al obtener información del router: {e}")
            return None

    def save_router_info(self, info):
        if info:
            try:
                with open(f'{info["nombre"]}_info.txt', 'w') as file:
                    for key, value in info.items():
                        file.write(f"{key.replace('_', ' ').title()}: {value}\n")
                print(f"Información guardada en {info['nombre']}_info.txt")
            except Exception as e:
                print(f"Error al guardar la información: {e}")

    def run(self):
        if self.connect_to_router():
            info = self.get_router_info()
            if info:
                self.save_router_info(info)

# Uso de la clase
if __name__ == "__main__":
    # Parámetros de conexión
    router_ip = "192.168.240.134"  # Cambia esto por la IP de tu equipo MikroTik
    username = "admin"         # Cambia esto por tu usuario
    password = "admin"              # Cambia esto por tu contraseña
    port = 4444                # Puerto API por defecto, cambia si es necesario

    # Crear instancia y ejecutar
    router_manager = RouterManager(router_ip, username, password, port)
    router_manager.run()