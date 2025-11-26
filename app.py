from flask import Flask
from flask_cors import CORS
from config.db_config import init_db
from routes import prediccion_routes, usuarios_routes


app = Flask(__name__)
CORS(app)

# Iniciar conexión a la base de datos
mysql = init_db(app)

# Asignar conexión a los módulos
usuarios_routes.mysql = mysql
prediccion_routes.mysql = mysql

# Registrar blueprints
app.register_blueprint(usuarios_routes.user_bp)
app.register_blueprint(prediccion_routes.predict_bp)


if __name__ == "__main__":
    app.run(debug=True, port=5000)