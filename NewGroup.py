from RouterManager import RouterManager
from librouteros.exceptions import TrapError

class NewGroup:
    def __init__(self, router_manager: RouterManager):
        self.router_manager = router_manager
        self.group_name = ""
        self.attributes = {}

    def set_group_name(self, name: str):
        """Establece el nombre del grupo."""
        self.group_name = name

    def set_attribute(self, key: str, value: str):
        """Establece un atributo para el grupo."""
        self.attributes[key] = value

    def create_group(self):
        """Crea el grupo en el router MikroTik."""
        if not self.router_manager.api:
            print("No hay conexión al router. Conectando...")
            if not self.router_manager.connect_to_router():
                print("No se pudo conectar al router.")
                return False

        if not self.group_name:
            print("Error: Nombre del grupo no especificado.")
            return False

        try:
            # Verificar si el grupo ya existe
            existing_groups = self.router_manager.api.path('user', 'group')
            if any(group['name'] == self.group_name for group in existing_groups):
                print(f"El grupo '{self.group_name}' ya existe.")
                return False

            # Crear el grupo
            group_params = {'name': self.group_name, **self.attributes}
            existing_groups.add(**group_params)
            print(f"Grupo '{self.group_name}' creado exitosamente.")
            return True
        except TrapError as e:
            print(f"Error al crear el grupo '{self.group_name}': {e}")
        except Exception as e:
            print(f"Error inesperado al crear el grupo '{self.group_name}': {e}")
        return False

    def run(self):
        """Ejecuta el proceso de creación del grupo."""
        return self.create_group()

# Ejemplo de uso
if __name__ == "__main__":
    router_ip = "192.168.240.134"
    username = "admin"
    password = "admin"
    port = 4444

    router_manager = RouterManager(router_ip, username, password, port)
    new_group = NewGroup(router_manager)

    # Configurar el nuevo grupo
    new_group.set_group_name("nuevo_grupo")
    new_group.set_attribute("policy", "read,write,policy,test")
    new_group.set_attribute("skin", "default")

    # Crear el grupo
    new_group.run()