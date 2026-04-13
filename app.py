# app.py - Punto de entrada de la aplicación

from flask import Flask, render_template, request, redirect, url_for, session, flash
from controllers.auth_controller import login_user_controller, logout_user
from controllers.registro_controller import registro_controller
from models.user_model import init_databases
from models.formulario_model import init_db_formularios, create_cliente

app = Flask(__name__)
app.secret_key = 'super_secret_key_progra4'
app.config['SESSION_PERMANENT'] = False

# Inicializar ambas bases de datos al arrancar la app
init_databases()
init_db_formularios()

@app.route('/')
def index():
    # Redirige la raíz al login
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtiene los datos del formulario de registro
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        nombre = request.form['nombre']
        apellido = request.form['apellido']

        # Llama al controller de registro
        success, message, user = registro_controller(username, password, email)
        flash(message)

        if success:
            # Guarda los datos del usuario en la sesión
            session['user_id'] = user[0]
            session['username'] = username
            session['nombre'] = nombre
            session['apellido'] = apellido
            # Redirige al formulario de cliente después del registro
            return redirect(url_for('client_form'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtiene las credenciales del formulario
        username = request.form['username']
        password = request.form['password']

        # Verifica las credenciales con el controller de autenticación
        success, message, user = login_user_controller(username, password)
        flash(message)

        if success:
            # Guarda el id y username en la sesión
            session['user_id'] = user[0]
            session['username'] = username
            return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Cierra la sesión y redirige al login
    logout_user()
    return redirect(url_for('login'))

@app.route('/client_form', methods=['GET', 'POST'])
def client_form():
    # Protege la ruta: solo usuarios autenticados pueden acceder
    if 'user_id' not in session:
        flash('Debes iniciar sesión primero')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Obtiene los datos del formulario de cliente
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        ocupacion = request.form['ocupacion']
        fecha_nacimiento = request.form['fecha_nacimiento']

        # Guarda el cliente usando nombre y apellido guardados en la sesión
        create_cliente(
            session['user_id'],
            session['nombre'],
            session['apellido'],
            telefono,
            direccion,
            ocupacion,
            fecha_nacimiento
        )
        flash('¡Cliente guardado correctamente!')
        return redirect(url_for('dashboard'))

    return render_template('client_form.html')

@app.route('/dashboard')
def dashboard():
    # Protege el dashboard: solo usuarios autenticados pueden verlo
    if 'user_id' not in session:
        flash('Debes iniciar sesión primero')
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

if __name__ == '__main__':
    app.run(debug=True)