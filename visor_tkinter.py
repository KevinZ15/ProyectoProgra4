import tkinter as tk
from tkinter import ttk
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_USERS = os.path.join(BASE_DIR, 'database', 'usuarios.db')
DB_CLIENTES = os.path.join(BASE_DIR, 'database', 'formularios.db')


def obtener_usuarios():
    conn = sqlite3.connect(DB_USERS)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users")
    data = cursor.fetchall()
    conn.close()
    return data


def obtener_clientes():
    conn = sqlite3.connect(DB_CLIENTES)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, usuario_id, nombre, apellido, telefono, direccion, ocupacion, fecha_nacimiento
        FROM clientes
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def cargar_datos():
    # limpiar tablas
    for row in tabla_usuarios.get_children():
        tabla_usuarios.delete(row)
    for row in tabla_clientes.get_children():
        tabla_clientes.delete(row)

    # cargar usuarios
    for u in obtener_usuarios():
        tabla_usuarios.insert("", "end", values=u)

    # cargar clientes
    for c in obtener_clientes():
        tabla_clientes.insert("", "end", values=c)

root = tk.Tk()
root.title("Visor de Usuarios y Clientes")

# ---- USUARIOS ----
tk.Label(root, text="Usuarios").pack()

tabla_usuarios = ttk.Treeview(root, columns=("id","username","email"), show="headings")
tabla_usuarios.heading("id", text="ID")
tabla_usuarios.heading("username", text="Usuario")
tabla_usuarios.heading("email", text="Email")
tabla_usuarios.pack(fill="x", padx=10, pady=5)

# ---- CLIENTES ----
tk.Label(root, text="Clientes").pack()

tabla_clientes = ttk.Treeview(root, columns=(
    "id","usuario_id","nombre","apellido","telefono","direccion","ocupacion","fecha_nacimiento"
), show="headings")

tabla_clientes.heading("id", text="ID")
tabla_clientes.heading("usuario_id", text="Usuario ID")
tabla_clientes.heading("nombre", text="Nombre")
tabla_clientes.heading("apellido", text="Apellido")
tabla_clientes.heading("telefono", text="Teléfono")
tabla_clientes.heading("direccion", text="Dirección")
tabla_clientes.heading("ocupacion", text="Ocupación")
tabla_clientes.heading("fecha_nacimiento", text="Nacimiento")

tabla_clientes.pack(fill="both", expand=True, padx=10, pady=5)

# botón
btn = tk.Button(root, text="Cargar datos", command=cargar_datos)
btn.pack(pady=10)

root.mainloop()