import openpyxl
from typing import List, Dict

class ExcelReader:
    def __init__(self, file_path: str, sheet_name: str = None):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.workbook = None
        self.sheet = None

    def load_workbook(self):
        """Carga el archivo Excel."""
        try:
            self.workbook = openpyxl.load_workbook(self.file_path)
            if self.sheet_name:
                self.sheet = self.workbook[self.sheet_name]
            else:
                self.sheet = self.workbook.active
        except Exception as e:
            print(f"Error al cargar el archivo Excel: {e}")
            raise

    def read_equipment_data(self) -> List[Dict[str, str]]:
        """Lee los datos de los equipos desde la hoja de cálculo."""
        if not self.sheet:
            self.load_workbook()

        equipment_data = []
        headers = [cell.value for cell in self.sheet[1]]

        for row in self.sheet.iter_rows(min_row=2, values_only=True):
            equipment = dict(zip(headers, row))
            if all(equipment.values()):  # Asegurarse de que todas las celdas tengan valor
                equipment_data.append(equipment)

        return equipment_data

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