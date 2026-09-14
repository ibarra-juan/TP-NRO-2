from interfaz_crud import CRUD

class Vehiculo(CRUD):
    def __init__(self):
        campos = ["Patente", "Marca", "Modelo", "Año", "Color"]
        super().__init__("Vehículo", campos, tabla_db="vehiculos", llave_primaria="Patente")


class Propietario(CRUD):
    def __init__(self):
        campos = ["DNI", "Nombre", "Apellido", "Telefono", "Email"]
        super().__init__("Propietario", campos, tabla_db="propietarios", llave_primaria="DNI")