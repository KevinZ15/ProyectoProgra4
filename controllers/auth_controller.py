from models.user_model import register_user, login_user

def register_user_controller(username, password, email):
    return register_user(username, password, email)

def login_user_controller(username, password):
    user = login_user(username, password)
    if user:
        return True, "Inicio de sesión exitoso", user
    return False, "Usuario o contraseña incorrectos", None

def logout_user():
    pass