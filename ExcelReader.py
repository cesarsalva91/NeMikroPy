import pandas as df
from typing import List, Dict

class ExcelReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None

    def read_equipment_data(self) -> List[Dict[str, str]]:
        """Lee los datos de los equipos desde la hoja de cálculo."""
        try:
            # Lee el archivo Excel directamente en un DataFrame de pandas
            self.data = df.read_excel(self.file_path)
            
            # Convierte el DataFrame a una lista de diccionarios
            equipment_data = self.data.to_dict('records')
            
            # Filtra las filas que tienen todos los valores
            equipment_data = [eq for eq in equipment_data if all(eq.values())]
            
            return equipment_data
        except Exception as e:
            print(f"Error al leer el archivo Excel: {e}")
            return []

    def print_equipment_data(self, data: List[Dict[str, str]]):
        """Imprime los datos de los equipos de forma legible."""
        for equipment in data:
            print("\nEquipo:")
            for key, value in equipment.items():
                print(f"  {key}: {value}")

if __name__ == "__main__":
    # Ejemplo de uso
    reader = ExcelReader("equipos.xlsx")
    data = reader.read_equipment_data()
    reader.print_equipment_data(data)