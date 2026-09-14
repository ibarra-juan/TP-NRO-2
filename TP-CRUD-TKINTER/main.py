# from entidades import Vehiculo, Propietario
# import tkinter as tk


# # --- Ventana principal ---
# root = tk.Tk()
# root.title("Menú Principal")
# root.geometry("400x250")
# root.configure(bg="#6286AA")      

# titulo = tk.Label(
#     root,
#     text="SELECCIONE\nLA BASE DE DATOS",
#     font=('Arial', 16, 'bold'),
#     fg="white",
#     bg="#6286AA"
# )
# titulo.pack(pady=20)

# # --- Funciones ---
# def ir_a_vehiculo():
#     app = Vehiculo()
#     root.destroy()
#     app.iniciar()

# def ir_a_propietario():
#     app = Propietario()
#     root.destroy()
#     app.iniciar()

# botones = tk.Frame(root, bg="#6286AA")
# botones.pack()

# boton_vehiculo = tk.Button(
#     botones,
#     text="Vehículo",
#     command=ir_a_vehiculo,
#     font=('Arial', 12, 'bold'),
#     bg="#3498DB",   
#     fg="white",
#     activebackground="#2980B9",
#     activeforeground="white",
#     width=12,
#     height=2
# )
# boton_vehiculo.pack(side=tk.LEFT, padx=10)

# boton_propietario = tk.Button(
#     botones,
#     text="Propietario",
#     command=ir_a_propietario,
#     font=('Arial', 12, 'bold'),
#     bg="#E74C3C",   
#     fg="white",
#     activebackground="#C0392B",
#     activeforeground="white",
#     width=12,
#     height=2
# )
# boton_propietario.pack(side=tk.RIGHT, padx=10)

# root.mainloop()



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
