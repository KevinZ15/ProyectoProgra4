# Proyecto Programación 4

Aplicación web desarrollada con Flask que permite registrar usuarios, gestionar clientes y visualizar datos mediante una interfaz de escritorio con Tkinter.

---

## Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.x | Lenguaje principal |
| Flask | Framework web |
| SQLite | Bases de datos |
| Tkinter | Interfaz gráfica de escritorio |

---

## Estructura del proyecto

    ProyectoProgra4/
    ├── app.py
    ├── visor_tkinter.py
    ├── models/
    │   ├── user_model.py
    │   └── formulario_model.py
    ├── controllers/
    │   ├── auth_controller.py
    │   └── registro_controller.py
    ├── templates/
    │   ├── login.html
    │   ├── register.html
    │   ├── client_form.html
    │   └── dashboard.html
    ├── static/
    └── database/
        ├── usuarios.db
        └── formularios.db

---

## Funcionalidades

- Registro e inicio de sesión de usuarios
- Creación de clientes asociados a un usuario
- Dashboard protegido por sesión
- Visualización de usuarios y clientes desde interfaz gráfica de escritorio

---

## Usuarios de prueba

Al iniciar la aplicación por primera vez, se crean automáticamente dos usuarios de prueba si no existen en la base de datos:

| Usuario | Contraseña | Email |
|---|---|---|---|
| `admin` | `admin123` | admin@prueba.com | 
| `usuario_prueba` | `prueba123` | usuario@prueba.com |

> Las contraseñas se almacenan cifradas con SHA-256. Los usuarios de prueba solo se crean si no existen, por lo que es seguro reiniciar la app sin perder datos.

---

## Instrucciones de ejecución

### 1. Requisitos previos

Asegurarse de tener Python 3.x instalado. Instalar Flask si no está disponible:

    pip install flask

### 2. Ejecutar la aplicación web

    python app.py

Abrir el navegador en `http://127.0.0.1:5000` y:

1. Iniciar sesión con un usuario de prueba, o registrar uno nuevo
2. Completar el formulario de cliente
3. Acceder al dashboard

### 3. Ejecutar el visor de escritorio

    python visor_tkinter.py

Presionar el botón **"Cargar datos"** para visualizar usuarios y clientes registrados.

---

## Notas

- No modificar las rutas de las bases de datos dentro del código
- Tkinter viene incluido por defecto en la mayoría de instalaciones de Python
- Las bases de datos se crean automáticamente en la carpeta `database/` si no existen