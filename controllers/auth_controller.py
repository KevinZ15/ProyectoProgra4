from functools import wraps
from flask import Blueprint, request, redirect, url_for, session, jsonify

from models.user_model import validate_user

auth_bp = Blueprint("auth", __name__)


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({
                "success": False,
                "message": "Debes iniciar sesion para acceder a esta ruta."
            }), 401
        return view_func(*args, **kwargs)
    return wrapped_view


@auth_bp.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "login"
    })


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or request.form

    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "Debes enviar username y password."
        }), 400

    user = validate_user(username, password)

    if user:
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["nombre"] = user["nombre"]
        session["apellido"] = user["apellido"]

        return jsonify({
            "success": True,
            "message": "Inicio de sesión correcto.",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "nombre": user["nombre"],
                "apellido": user["apellido"],
                "correo": user["correo"]
            }
        })

    return jsonify({
        "success": False,
        "message": "Usuario o contraseña incorrectos."
    }), 401


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return jsonify({
        "success": True,
        "message": "Sesión cerrada correctamente."
    })


@auth_bp.route("/session", methods=["GET"])
def session_status():
    if "user_id" in session:
        return jsonify({
            "authenticated": True,
            "user": {
                "id": session.get("user_id"),
                "username": session.get("username"),
                "nombre": session.get("nombre"),
                "apellido": session.get("apellido")
            }
        })

    return jsonify({
        "authenticated": False
    })


@auth_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return jsonify({
        "success": True,
        "message": "Acceso autorizado al dashboard.",
        "user": {
            "id": session.get("user_id"),
            "username": session.get("username"),
            "nombre": session.get("nombre"),
            "apellido": session.get("apellido")
        }
    })