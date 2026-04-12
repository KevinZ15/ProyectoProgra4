# controllers/registro_controller.py

from flask import Blueprint, request, redirect, url_for, session, jsonify
from models.user_model import create_user, get_user_by_username
from models.formulario_model import create_cliente

registro_bp = Blueprint("registro", __name__)

# Ruta para registrar un nuevo usuario
@registro_bp.route("/registro", methods=["POST"])
def registro():
    data = request.get_json(silent=True) or request.form

    username = data.get("username", "").strip()
    correo = data.get("correo", "").strip()
    nombre = data.get("nombre", "").strip()
    apellido = data.get("apellido", "").strip()
    password = data.get("password", "").strip()

    # Validar que todos los campos estén llenos
    if not username or not correo or not nombre or not apellido or not password:
        return jsonify({
            "success": False,
            "message": "Todos los campos son obligatorios."
        }), 400

    exito, mensaje = create_user(username, correo, nombre, apellido, password)

    if not exito:
        return jsonify({
            "success": False,
            "message": mensaje
        }), 400

    # Iniciar sesión automáticamente después del registro
    user = get_user_by_username(username)
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["nombre"] = user["nombre"]
    session["apellido"] = user["apellido"]

    return jsonify({
        "success": True,
        "message": "Registro exitoso.",
        "redirect": "/formulario-cliente"
    })


# Ruta para guardar el formulario de cliente
@registro_bp.route("/formulario-cliente", methods=["POST"])
def formulario_cliente():
    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Debes registrarte primero."
        }), 401

    data = request.get_json(silent=True) or request.form

    telefono = data.get("telefono", "").strip()
    direccion = data.get("direccion", "").strip()
    ocupacion = data.get("ocupacion", "").strip()
    fecha_nacimiento = data.get("fecha_nacimiento", "").strip()

    if not telefono or not direccion or not ocupacion or not fecha_nacimiento:
        return jsonify({
            "success": False,
            "message": "Todos los campos son obligatorios."
        }), 400

    # Obtener el id del usuario desde la sesión
    usuario_id = session["user_id"]
    create_cliente(usuario_id, telefono, direccion, ocupacion, fecha_nacimiento)

    return jsonify({
        "success": True,
        "message": "Formulario guardado correctamente.",
        "redirect": "/dashboard"
    })