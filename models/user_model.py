import sqlite3
import hashlib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_USERS = os.path.join(BASE_DIR, '..', 'database', 'usuarios.db')
DB_FORMS = os.path.join(BASE_DIR, '..', 'database', 'formularios.db')

def init_databases():
    os.makedirs(os.path.dirname(DB_USERS), exist_ok=True)
    
    # Tabla usuarios
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    
    # Tabla clientes
    conn = sqlite3.connect(DB_FORMS)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT,
                    apellido TEXT,
                    email TEXT,
                    telefono TEXT,
                    direccion TEXT)''')
    conn.commit()
    conn.close()

def hash_password(password):
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
        return False, "El usuario ya existe"
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
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

def save_client(nombre, apellido, email, telefono, direccion):
    conn = sqlite3.connect(DB_FORMS)
    c = conn.cursor()
    c.execute("""INSERT INTO clientes (nombre, apellido, email, telefono, direccion)
                 VALUES (?, ?, ?, ?, ?)""", (nombre, apellido, email, telefono, direccion))
    conn.commit()
    conn.close()