Proyecto
TECNOLOGÍAS UTILIZADAS

Python 3.x
Flask (framework web)
Tkinter (interfaz gráfica de escritorio)
SQLite (bases de datos)

app.py → Aplicación principal en Flask
visor_tkinter.py → Visor de datos en Tkinter
models/ → Lógica de acceso a datos
controllers/ → Controladores de la aplicación
templates/ → Vistas HTML (Flask)
database/usuarios.db → Base de datos de usuarios
database/formularios.db → Base de datos de clientes

FUNCIONALIDADES

Registro de usuarios
Inicio de sesión
Creación de clientes asociados a un usuario
Visualización de usuarios y clientes mediante interfaz gráfica

INSTRUCCIONES DE EJECUCIÓN

Ejecutar la aplicación web:

python app.py

Abrir en el navegador:

Registrar un usuario
Iniciar sesión
Crear un cliente

Ejecutar el visor de escritorio:

python visor_tkinter.py

Presionar el botón "Cargar datos" para visualizar la información

NOTAS

Asegurarse de tener Python instalado
Tkinter viene incluido por defecto en la mayoría de instalaciones de Python
No modificar las rutas de las bases de datos