from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from controllers.auth_controller import register_user_controller, login_user_controller, logout_user
from models.user_model import init_databases, get_user_by_username

app = Flask(__name__)
app.secret_key = 'super_secret_key_progra4'
app.config['SESSION_PERMANENT'] = False 
# Crear bases de datos al iniciar
init_databases()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        success, message = register_user_controller(username, password, email)
        flash(message)
        if success:
            user = get_user_by_username(username)
            session['user_id'] = user[0]
            session['username'] = username
            return redirect(url_for('client_form'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        success, message, user = login_user_controller(username, password)
        flash(message)
        if success:
            session['user_id'] = user[0]
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/client_form', methods=['GET', 'POST'])
def client_form():
    if 'user_id' not in session:
        flash('Debes iniciar sesión primero')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        
        from models.user_model import save_client
        save_client(nombre, apellido, email, telefono, direccion)
        flash('¡Cliente guardado correctamente!')
        return redirect(url_for('dashboard'))
    
    return render_template('client_form.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Debes iniciar sesión primero')
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

if __name__ == '__main__':
    app.run(debug=True)