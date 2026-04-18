# models/user_model.py

import sqlite3
import hashlib
import os

# Ruta absoluta a la base de datos, relativa a la ubicación de este archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_USERS = os.path.join(BASE_DIR, '..', 'database', 'usuarios.db')

# Usuarios de prueba que se insertan automáticamente al iniciar la app
SEED_USERS = [
    {
        'username': 'admin',
        'password': 'admin123',
        'email': 'admin@prueba.com'
    },
    {
        'username': 'usuario_prueba',
        'password': 'prueba123',
        'email': 'usuario@prueba.com'
    }
]

def init_databases():
    os.makedirs(os.path.dirname(DB_USERS), exist_ok=True)

    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    # Crea la tabla solo si no existe, evita error si ya fue creada antes
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL)''')
    conn.commit()
    conn.close()

    _seed_users()

def _seed_users():
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    for u in SEED_USERS:
        # Verifica si el usuario ya existe antes de intentar insertarlo
        c.execute("SELECT id FROM users WHERE username = ?", (u['username'],))
        if c.fetchone() is None:
            # Guarda la contraseña hasheada, nunca en texto plano
            c.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (u['username'], hash_password(u['password']), u['email'])
            )
            print(f"[Seed] Usuario de prueba creado: {u['username']} / {u['password']}")
    conn.commit()
    conn.close()

def hash_password(password):
    # Convierte la contraseña a SHA-256; el resultado es siempre una cadena de 64 caracteres
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, email):
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                  (username, hash_password(password), email))
        conn.commit()
        return True, "Usuario registrado con éxito"
    except sqlite3.IntegrityError:
        # Salta cuando el username ya existe por la restricción UNIQUE
        return False, "El usuario ya existe"
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    # Compara hasheando la contraseña ingresada para verificar contra la almacenada
    c.execute("SELECT id, username FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user

def get_user_by_username(username):
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user