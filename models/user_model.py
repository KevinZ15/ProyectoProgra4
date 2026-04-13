# models/user_model.py

import sqlite3
import hashlib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_USERS = os.path.join(BASE_DIR, '..', 'database', 'usuarios.db')

def init_databases():
    # Crea el directorio database/ si no existe
    os.makedirs(os.path.dirname(DB_USERS), exist_ok=True)

    # Crea la tabla de usuarios si no existe
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def hash_password(password):
    # Encripta la contraseña usando SHA-256 antes de guardarla
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, email):
    # Inserta un nuevo usuario en la base de datos
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                  (username, hash_password(password), email))
        conn.commit()
        return True, "Usuario registrado con éxito"
    except sqlite3.IntegrityError:
        # El username ya existe en la base de datos
        return False, "El usuario ya existe"
    finally:
        conn.close()

def login_user(username, password):
    # Busca el usuario verificando username y contraseña hasheada
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    c.execute("SELECT id, username FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user

def get_user_by_username(username):
    # Retorna todos los datos del usuario según su username
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user