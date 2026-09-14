import mariadb
import sys
from tkinter import messagebox

class ConexionDB:
    def __init__(self, user="root", password="", host="127.0.0.1", port=3306, database="gestion_vehiculos"):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def conectar(self):
        try:
            conexion = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            return conexion
        except mariadb.Error as error:
            messagebox.showerror("Error de Conexión", f"Error al conectar a MariaDB: {error}")
            sys.exit(1)
