from flask import session
from models.user_model import login_user

def login_user_controller(username, password):
    # Verifica las credenciales contra la base de datos
    user = login_user(username, password)
    
    # Retorna éxito si el usuario existe y la contraseña es correcta
    if user:
        return True, "Inicio de sesión exitoso", user
    
    # Retorna error si las credenciales no coinciden
    return False, "Usuario o contraseña incorrectos", None

def logout_user():
    # Limpia todos los datos de la sesión activa
    session.clear()