import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FORMS = os.path.join(BASE_DIR, '..', 'database', 'formularios.db')

def get_connection():
    # Crea el directorio si no existe y retorna la conexión a la BD
    os.makedirs(os.path.dirname(DB_FORMS), exist_ok=True)
    conn = sqlite3.connect(DB_FORMS)
    conn.row_factory = sqlite3.Row
    return conn

def init_db_formularios():
    # Crea la tabla clientes si no existe
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT NOT NULL,
            direccion TEXT NOT NULL,
            ocupacion TEXT NOT NULL,
            fecha_nacimiento TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def create_cliente(usuario_id, nombre, apellido, telefono, direccion, ocupacion, fecha_nacimiento):
    # Inserta un nuevo cliente vinculado al usuario registrado
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (usuario_id, nombre, apellido, telefono, direccion, ocupacion, fecha_nacimiento)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (usuario_id, nombre, apellido, telefono, direccion, ocupacion, fecha_nacimiento))
    conn.commit()
    conn.close()
    return True

def get_cliente_by_usuario(usuario_id):
    # Busca y retorna el cliente según su usuario_id
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE usuario_id = ?", (usuario_id,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente