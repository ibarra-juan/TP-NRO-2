import tkinter as tk
from tkinter import messagebox
import mariadb
from conexion_bd import ConexionDB  



class CRUD:
    def __init__(self, entidad, campos, tabla_db, llave_primaria):
        self.entidad = entidad
        self.campos = campos
        self.tabla_db = tabla_db
        self.llave_primaria = llave_primaria
        self.entries = {}
        self.ventana = None
        self.db = ConexionDB()
        
    def iniciar(self):
        self.crear_tabla_si_no_existe()
        self.ventana = tk.Tk()
        self.ventana.title(f"Gestión de {self.entidad}")
        self.ventana.resizable(False, False)
        
        self.crear_titulo()
        self.crear_formulario()
        self.crear_botones()
        
        self.ventana.mainloop()

    def crear_tabla_si_no_existe(self):
        conn = self.db.conectar()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            sql_create = f"CREATE TABLE IF NOT EXISTS {self.tabla_db} ({self.llave_primaria} VARCHAR(50) PRIMARY KEY)"
            cursor.execute(sql_create)

            cursor.execute(f"SHOW COLUMNS FROM {self.tabla_db}")
            columnas_existentes = [row[0] for row in cursor.fetchall()]

            for campo in self.campos:
                if campo not in columnas_existentes:
                    sql_alter = f"ALTER TABLE {self.tabla_db} ADD COLUMN {campo} VARCHAR(100)"
                    cursor.execute(sql_alter)

            conn.commit()
        except mariadb.Error as e:
            messagebox.showerror("Error SQL", f"Error al sincronizar tabla: {e}")
        finally:
            conn.close()

    def crear_titulo(self):
        titulo = tk.Label(self.ventana, text=f"Gestión de {self.entidad}", font=('Arial', 14, 'bold'))
        titulo.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

    def crear_formulario(self):
        for i, campo in enumerate(self.campos, start=1):
            etiqueta = tk.Label(self.ventana, text=f"{campo}:", anchor="e")
            etiqueta.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            
            entrada = tk.Entry(self.ventana, width=25)
            entrada.grid(row=i, column=1, padx=10, pady=5)
            self.entries[campo] = entrada

    def crear_botones(self):
        frame_botones = tk.Frame(self.ventana)
        fila_inicio = len(self.campos) + 1
        frame_botones.grid(row=fila_inicio, column=0, columnspan=2, pady=15)

        tk.Button(frame_botones, text="Crear", width=10, command=self.crear).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_botones, text="Buscar", width=10, command=self.leer).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_botones, text="Modificar", width=10, command=self.actualizar).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_botones, text="Eliminar", width=10, command=self.eliminar).pack(side=tk.LEFT, padx=3)
        tk.Button(frame_botones, text="Volver", width=10, command=self.volver).pack(side=tk.LEFT, padx=3)

    def obtener_datos(self):
        datos = {}
        for campo, entry in self.entries.items():
            valor = entry.get().strip()
            if not valor:  # Validación de campo vacío
                messagebox.showerror("Error", f"El campo '{campo}' no puede estar vacío.")
                return None  # Si hay error, devolvemos None
            datos[campo] = valor
        return datos

    def limpiar_formulario(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def crear(self):
        datos = self.obtener_datos()
        if datos is None:  # Si hubo campos vacíos, se corta
            return
        columnas = ", ".join(datos.keys())
        placeholders = ", ".join(["%s"] * len(datos))
        sql = f"INSERT INTO {self.tabla_db} ({columnas}) VALUES ({placeholders})"

        conn = self.db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql, list(datos.values()))
                conn.commit()
                messagebox.showinfo("Éxito", f"{self.entidad} guardado.")
                self.limpiar_formulario()
            except mariadb.Error as e:
                messagebox.showerror("Error SQL", f"No se pudo guardar: {e}")
            finally:
                conn.close()

    def leer(self):
        id_valor = self.entries[self.llave_primaria].get()
        if not id_valor:
            messagebox.showwarning("Atención", f"Ingrese '{self.llave_primaria}' para buscar.")
            return

        sql = f"SELECT {', '.join(self.campos)} FROM {self.tabla_db} WHERE {self.llave_primaria} = %s"
        conn = self.db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql, (id_valor,))
                fila = cursor.fetchone()
                if fila:
                    for campo, valor in zip(self.campos, fila):
                        self.entries[campo].delete(0, tk.END)
                        self.entries[campo].insert(0, str(valor))
                    messagebox.showinfo("Éxito", "Registro encontrado.")
                else:
                    messagebox.showwarning("Sin resultados", "No se encontró el registro.")
            except mariadb.Error as e:
                messagebox.showerror("Error SQL", f"Error en lectura: {e}")
            finally:
                conn.close()

    def actualizar(self):
        datos = self.obtener_datos()
        id_valor = datos.get(self.llave_primaria)
        if not id_valor:
            messagebox.showwarning("Atención", f"Ingrese '{self.llave_primaria}'.")
            return

        set_clause = ", ".join([f"{campo} = %s" for campo in datos.keys()])
        sql = f"UPDATE {self.tabla_db} SET {set_clause} WHERE {self.llave_primaria} = %s"
        valores = list(datos.values()) + [id_valor]

        conn = self.db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql, valores)
                conn.commit()
                messagebox.showinfo("Éxito", f"{self.entidad} actualizado.")
            except mariadb.Error as e:
                messagebox.showerror("Error SQL", f"No se pudo actualizar: {e}")
            finally:
                conn.close()

    def eliminar(self):
        id_valor = self.entries[self.llave_primaria].get()
        if not id_valor:
            messagebox.showwarning("Atención", f"Ingrese '{self.llave_primaria}'.")
            return

        if not messagebox.askyesno("Confirmar", "¿Desea eliminar el registro?"):
            return

        sql = f"DELETE FROM {self.tabla_db} WHERE {self.llave_primaria} = %s"
        conn = self.db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql, (id_valor,))
                conn.commit()
                messagebox.showinfo("Éxito", "Registro eliminado.")
                self.limpiar_formulario()
            except mariadb.Error as e:
                messagebox.showerror("Error SQL", f"No se pudo eliminar: {e}")
            finally:
                conn.close()

    def volver(self):
        self.ventana.destroy()
        from main import MenuPrincipal
        MenuPrincipal()
