from flask_mysqldb import MySQL

def init_db(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''  # sin contraseña
    app.config['MYSQL_DB'] = 'proyecto_ia'
    mysql = MySQL(app)
    return mysql
