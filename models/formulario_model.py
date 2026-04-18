import os
import sqlite3

# Ruta absoluta a la base de datos, relativa a la ubicación de este archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FORMS = os.path.join(BASE_DIR, '..', 'database', 'formularios.db')

# Datos de prueba que se insertan automáticamente al iniciar la app
SEED_CLIENTES = [
    {
        'username': 'admin',
        'nombre': 'Administrador',
        'apellido': 'Sistema',
        'telefono': '8888-0001',
        'direccion': 'San Jose, Costa Rica',
        'ocupacion': 'Administrador',
        'fecha_nacimiento': '1990-01-15'
    },
    {
        'username': 'usuario_prueba',
        'nombre': 'Usuario',
        'apellido': 'Prueba',
        'telefono': '8888-0002',
        'direccion': 'Cartago, Costa Rica',
        'ocupacion': 'Estudiante',
        'fecha_nacimiento': '2000-06-20'
    }
]

def get_connection():
    os.makedirs(os.path.dirname(DB_FORMS), exist_ok=True)
    conn = sqlite3.connect(DB_FORMS)
    # row_factory permite acceder a las columnas por nombre en vez de por índice
    conn.row_factory = sqlite3.Row
    return conn

def init_db_formularios():
    conn = get_connection()
    cursor = conn.cursor()
    # Crea la tabla solo si no existe, evita error si ya fue creada antes
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

def seed_formularios(get_user_id_fn):
    conn = get_connection()
    cursor = conn.cursor()
    for cliente in SEED_CLIENTES:
        # Busca el usuario en la BD de usuarios usando la función recibida como parámetro
        user = get_user_id_fn(cliente['username'])
        if user is None:
            continue
        usuario_id = user[0]
        # Solo inserta si ese usuario todavía no tiene formulario registrado
        cursor.execute("SELECT id FROM clientes WHERE usuario_id = ?", (usuario_id,))
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO clientes (usuario_id, nombre, apellido, telefono, direccion, ocupacion, fecha_nacimiento)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                usuario_id,
                cliente['nombre'],
                cliente['apellido'],
                cliente['telefono'],
                cliente['direccion'],
                cliente['ocupacion'],
                cliente['fecha_nacimiento']
            ))
            print(f"[Seed] Formulario de prueba creado para usuario: {cliente['username']}")
    conn.commit()
    conn.close()

def create_cliente(usuario_id, nombre, apellido, telefono, direccion, ocupacion, fecha_nacimiento):
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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE usuario_id = ?", (usuario_id,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente