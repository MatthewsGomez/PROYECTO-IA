from flask_mysqldb import MySQL
from flask_mail import Mail
import os

def init_db(app):
    # Cargar configuración SOLO desde variables de entorno
    # No hay valores por defecto con credenciales reales
    app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
    app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'usuario_desarrollo')
    app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'password_desarrollo')
    app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'basedatos_desarrollo')
    app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))
    
    # Verificar que todas las variables estén configuradas
    required_vars = ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DB']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        raise Exception(f"Faltan variables de entorno: {', '.join(missing_vars)}")
    
    mysql = MySQL(app)
    return mysql