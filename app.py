from flask import Flask
from controllers.auth_controller import auth_bp
from models.user_model import init_db

app = Flask(__name__)
app.secret_key = "clave_secreta_proyecto_progra4"

init_db()
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)