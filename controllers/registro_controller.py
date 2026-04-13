from models.user_model import register_user, get_user_by_username

def registro_controller(username, password, email):
    # Intenta registrar el usuario en la base de datos
    success, message = register_user(username, password, email)
    
    # Si el registro falló, retorna el error sin continuar
    if not success:
        return False, message, None

    # Obtiene los datos del usuario recién creado
    user = get_user_by_username(username)
    return True, message, user