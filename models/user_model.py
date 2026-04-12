import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "usuarios.db")


def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            correo TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def create_user(username, correo, nombre, apellido, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuarios (username, correo, nombre, apellido, password)
            VALUES (?, ?, ?, ?, ?)
        """, (username, correo, nombre, apellido, password))
        conn.commit()
        return True, "Usuario registrado correctamente."
    except sqlite3.IntegrityError:
        return False, "El username o el correo ya existen."
    finally:
        conn.close()


def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM usuarios
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()
    conn.close()
    return user


def validate_user(username, password):
    user = get_user_by_username(username)

    if user and user["password"] == password:
        return user

    return None