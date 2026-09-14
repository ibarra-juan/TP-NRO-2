
import tkinter as tk
from entidades import Vehiculo, Propietario

class MenuPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Menú Principal")
        self.root.geometry("400x250")
        self.root.configure(bg="#6286AA")

        titulo = tk.Label(
            self.root,
            text="SELECCIONE\nLA BASE DE DATOS",
            font=('Arial', 16, 'bold'),
            fg="white",
            bg="#6286AA"
        )
        titulo.pack(pady=20)

        botones = tk.Frame(self.root, bg="#6286AA")
        botones.pack()

        tk.Button(
            botones,
            text="Vehículo",
            command=self.ir_a_vehiculo,
            font=('Arial', 12, 'bold'),
            bg="#3498DB", fg="white",
            width=12, height=2
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            botones,
            text="Propietario",
            command=self.ir_a_propietario,
            font=('Arial', 12, 'bold'),
            bg="#E74C3C", fg="white",
            width=12, height=2
        ).pack(side=tk.RIGHT, padx=10)

        self.root.mainloop()


    def ir_a_vehiculo(self):
        self.root.destroy()
        app = Vehiculo()
        app.iniciar()

    def ir_a_propietario(self):
        self.root.destroy()
        app = Propietario()
        app.iniciar()

if __name__ == "__main__":
    MenuPrincipal()
