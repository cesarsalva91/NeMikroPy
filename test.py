from librouteros import connect
from librouteros.exceptions import TrapError

def connect_to_router(router_ip, username, password):
    try:
        # Conexión al router MikroTik
        api = connect(username=username, password=password, host=router_ip)
        return api
    except TrapError as e:
        print(f"Error en MikroTik API (TrapError) al conectar con {router_ip}: {e}")
    except Exception as e:
        print(f"Error inesperado al conectar con {router_ip}: {e}")
    return None

def get_router_info(api, router_ip):
    try:
        # Obtener información del sistema
        identity = api.path('system', 'identity')
        system_resource = api.path('system', 'resource')
        
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
            'ip_router': router_ip
        }
    except Exception as e:
        print(f"Error al obtener información del router: {e}")
        return None

def save_router_info(info):
    if info:
        try:
            with open(f'{info["nombre"]}_info.txt', 'w') as file:
                for key, value in info.items():
                    file.write(f"{key.replace('_', ' ').title()}: {value}\n")
            print(f"Información guardada en {info['nombre']}_info.txt")
        except Exception as e:
            print(f"Error al guardar la información: {e}")

def main(router_ip, username, password):
    api = connect_to_router(router_ip, username, password)
    if api:
        info = get_router_info(api, router_ip)
        if info:
            save_router_info(info)

# Parámetros de conexión
router_ip = "192.168.240.134"  # Cambia esto por la IP de tu equipo MikroTik
username = "admin"         # Cambia esto por tu usuario
password = "admin"              # Cambia esto por tu contraseña

# Llamada a la función principal
main(router_ip, username, password)
