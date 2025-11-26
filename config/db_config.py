from flask_mysqldb import MySQL
from flask_mail import Mail
import os

def init_db(app):
    app.config['MYSQL_HOST'] = 'bsiamiq4tnd2zfjvfe1e-mysql.services.clever-cloud.com'
    app.config['MYSQL_USER'] = 'ux7dua5mflupv0ub'
    app.config['MYSQL_PASSWORD'] = 'ux7dua5mflupv0ub'
    app.config['MYSQL_DB'] = 'bsiamiq4tnd2zfjvfe1e'
    app.config['MYSQL_PORT'] = 3306
    mysql = MySQL(app)
    return mysql
