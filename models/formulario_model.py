import os
import sqlite3

# Ruta de la base de datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "formularios.db")

# Conexión a la base de datos
def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Crea la tabla clientes si no existe
def init_db_formularios():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            telefono TEXT NOT NULL,
            direccion TEXT NOT NULL,
            ocupacion TEXT NOT NULL,
            fecha_nacimiento TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Guarda un nuevo cliente en la base de datos
def create_cliente(usuario_id, telefono, direccion, ocupacion, fecha_nacimiento):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (usuario_id, telefono, direccion, ocupacion, fecha_nacimiento)
        VALUES (?, ?, ?, ?, ?)
    """, (usuario_id, telefono, direccion, ocupacion, fecha_nacimiento))
    conn.commit()
    conn.close()
    return True


# Busca un cliente por su usuario_id
def get_cliente_by_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM clientes WHERE usuario_id = ?
    """, (usuario_id,))

    cliente = cursor.fetchone()
    conn.close()
    return cliente