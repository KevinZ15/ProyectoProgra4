from flask import Flask
from controllers.auth_controller import auth_bp
from controllers.registro_controller import registro_bp
from models.user_model import init_db
from models.formulario_model import init_db_formularios

app = Flask(__name__)

# Clave secreta para manejar las sesiones
app.secret_key = "clave_secreta_proyecto_progra4"

# Inicializar las bases de datos al arrancar la app
init_db()
init_db_formularios()

# Registrar los blueprints de autenticación y registro
app.register_blueprint(auth_bp)
app.register_blueprint(registro_bp)

if __name__ == "__main__":
    app.run(debug=True)