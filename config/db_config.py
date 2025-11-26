from flask_mysqldb import MySQL
from flask_mail import Mail
import os

def init_db(app):
    app.config['MYSQL_HOST'] = 'b9qmehaxhy6yjls3pnt3-mysql.services.clever-cloud.com'
    app.config['MYSQL_USER'] = 'unjbftdqf3uullb7'
    app.config['MYSQL_PASSWORD'] = '7MRLPzHRMDHukCwYNgAE'
    app.config['MYSQL_DB'] = 'b9qmehaxhy6yjls3pnt3'
    app.config['MYSQL_PORT'] = 3306
    mysql = MySQL(app)
    return mysql

def init_mail(app):
    # Configuración de Flask-Mail
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # Tu correo
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # Tu contraseña de aplicación
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
    
    mail = Mail(app)
    return mail