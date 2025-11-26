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
