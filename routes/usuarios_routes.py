from flask import Blueprint, request, jsonify
from flask_mail import Message
from utils.pdf_generator import generar_pdf_historial

# Variable mysql que se asignará desde app.py
mysql = None
mail = None

user_bp = Blueprint('user_routes', __name__)

# ==============================
# Ruta para obtener todos los usuarios (opcional)
# ==============================
@user_bp.route("/users", methods=["GET"])
def get_users():
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT id, usuario FROM usuarios")
            data = cursor.fetchall()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==============================
# Registro de usuario
# ==============================
@user_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    usuario = data.get("usuario")
    contraseña = data.get("contraseña")

    if not usuario or not contraseña:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO usuarios (usuario, contrseña) VALUES (%s, %s)",
                (usuario, contraseña)
            )
            mysql.connection.commit()
            id_usuario = cursor.lastrowid
        return jsonify({"mensaje": "Usuario registrado correctamente", "id_usuario": id_usuario}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==============================
# Login de usuario
# ==============================
@user_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    usuario = data.get("usuario")
    contraseña = data.get("contraseña")

    if not usuario or not contraseña:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM usuarios WHERE usuario=%s AND contrseña=%s",
                (usuario, contraseña)
            )
            fila = cursor.fetchone()
        if fila:
            id_usuario = fila[0]
            return jsonify({"mensaje": "Login exitoso", "id_usuario": id_usuario}), 200
        else:
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==============================
# Historial del usuario
# ==============================
@user_bp.route("/historial/<int:id_usuario>", methods=["GET"])
def historial_usuario(id_usuario):
    from mappings import accident_severity, day_of_week, junction_control, junction_detail, light_conditions, local_authority, road_surface_conditions, road_type, speed_limit, urban_or_rural_area, weather_conditions, vehicle_type, number_of_casualties, number_of_vehicles

    severity_emojis = {0: "💚", 1: "🚨", 2: "🚑"}

    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    r.id,
                    r.fecha_respuesta,
                    r.Day_of_Week,
                    r.Junction_Control,
                    r.Junction_Detail,
                    r.Light_Conditions,
                    r.Local_Authority_District,
                    r.Road_Surface_Conditions,
                    r.Road_Type,
                    r.Speed_limit,
                    r.Urban_or_Rural_Area,
                    r.Weather_Conditions,
                    r.Vehicle_Type,
                    r.Number_of_Casualties,
                    r.Number_of_Vehicles,
                    p.modelo_RF,
                    p.modelo_KNN,
                    p.modelo_SVM,
                    p.fecha_prediccion
                FROM respuestas r
                JOIN predicciones p ON r.id = p.id_respuestas
                WHERE r.id_usuario = %s
                ORDER BY r.fecha_respuesta DESC
            """, (id_usuario,))
            datos = cursor.fetchall()

        if not datos:
            return jsonify({"mensaje": "No hay registros para este usuario"}), 404

        historial = []
        for fila in datos:
            historial.append({
                "id_respuesta": fila[0],
                "fecha_respuesta": str(fila[1]),
                "datos_ingresados": {
                    "Day_of_Week": day_of_week.get(fila[2], fila[2]),
                    "Junction_Control": junction_control.get(fila[3], fila[3]),
                    "Junction_Detail": junction_detail.get(fila[4], fila[4]),
                    "Light_Conditions": light_conditions.get(fila[5], fila[5]),
                    "Local_Authority_District": local_authority.get(fila[6], fila[6]),
                    "Road_Surface_Conditions": road_surface_conditions.get(fila[7], fila[7]),
                    "Road_Type": road_type.get(fila[8], fila[8]),
                    "Speed_limit": speed_limit.get(fila[9], fila[9]),
                    "Urban_or_Rural_Area": urban_or_rural_area.get(fila[10], fila[10]),
                    "Weather_Conditions": weather_conditions.get(fila[11], fila[11]),
                    "Vehicle_Type": vehicle_type.get(fila[12], fila[12]),
                    "Number_of_Casualties": number_of_casualties.get(fila[13], fila[13]),
                    "Number_of_Vehicles": number_of_vehicles.get(fila[14], fila[14]),
                },
                "predicciones": {
                    "RandomForest": f"{severity_emojis.get(fila[15],'❓')} {accident_severity.get(fila[15],'Desconocido')}",
                    "KNN": f"{severity_emojis.get(fila[16],'❓')} {accident_severity.get(fila[16],'Desconocido')}",
                    "SVM": f"{severity_emojis.get(fila[17],'❓')} {accident_severity.get(fila[17],'Desconocido')}",
                    "fecha_prediccion": str(fila[18])
                }
            })

        return jsonify({"id_usuario": id_usuario, "historial": historial}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==============================
# Enviar historial por email
# ==============================
@user_bp.route("/enviar_historial", methods=["POST"])
def enviar_historial_email():
    """
    Endpoint para enviar el historial del usuario en PDF por correo electrónico
    Body: {
        "id_usuario": 123,
        "email": "usuario@example.com"
    }
    """
    data = request.get_json()
    id_usuario = data.get("id_usuario")
    email_destino = data.get("email")
    
    if not id_usuario or not email_destino:
        return jsonify({"error": "Faltan datos: id_usuario y email son requeridos"}), 400
    
    try:
        # Obtener el nombre de usuario
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT usuario FROM usuarios WHERE id=%s", (id_usuario,))
            usuario_data = cursor.fetchone()
            
        if not usuario_data:
            return jsonify({"error": "Usuario no encontrado"}), 404
            
        nombre_usuario = usuario_data[0]
        
        # Obtener el historial usando la función existente
        from mappings import accident_severity, day_of_week, junction_control, junction_detail, light_conditions, local_authority, road_surface_conditions, road_type, speed_limit, urban_or_rural_area, weather_conditions, vehicle_type, number_of_casualties, number_of_vehicles

        severity_emojis = {0: "💚", 1: "🚨", 2: "🚑"}

        with mysql.connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    r.id,
                    r.fecha_respuesta,
                    r.Day_of_Week,
                    r.Junction_Control,
                    r.Junction_Detail,
                    r.Light_Conditions,
                    r.Local_Authority_District,
                    r.Road_Surface_Conditions,
                    r.Road_Type,
                    r.Speed_limit,
                    r.Urban_or_Rural_Area,
                    r.Weather_Conditions,
                    r.Vehicle_Type,
                    r.Number_of_Casualties,
                    r.Number_of_Vehicles,
                    p.modelo_RF,
                    p.modelo_KNN,
                    p.modelo_SVM,
                    p.fecha_prediccion
                FROM respuestas r
                JOIN predicciones p ON r.id = p.id_respuestas
                WHERE r.id_usuario = %s
                ORDER BY r.fecha_respuesta DESC
            """, (id_usuario,))
            datos = cursor.fetchall()

        if not datos:
            return jsonify({"error": "No hay registros para este usuario"}), 404

        historial = []
        for fila in datos:
            historial.append({
                "id_respuesta": fila[0],
                "fecha_respuesta": str(fila[1]),
                "datos_ingresados": {
                    "Day_of_Week": day_of_week.get(fila[2], fila[2]),
                    "Junction_Control": junction_control.get(fila[3], fila[3]),
                    "Junction_Detail": junction_detail.get(fila[4], fila[4]),
                    "Light_Conditions": light_conditions.get(fila[5], fila[5]),
                    "Local_Authority_District": local_authority.get(fila[6], fila[6]),
                    "Road_Surface_Conditions": road_surface_conditions.get(fila[7], fila[7]),
                    "Road_Type": road_type.get(fila[8], fila[8]),
                    "Speed_limit": speed_limit.get(fila[9], fila[9]),
                    "Urban_or_Rural_Area": urban_or_rural_area.get(fila[10], fila[10]),
                    "Weather_Conditions": weather_conditions.get(fila[11], fila[11]),
                    "Vehicle_Type": vehicle_type.get(fila[12], fila[12]),
                    "Number_of_Casualties": number_of_casualties.get(fila[13], fila[13]),
                    "Number_of_Vehicles": number_of_vehicles.get(fila[14], fila[14]),
                },
                "predicciones": {
                    "RandomForest": f"{severity_emojis.get(fila[15],'❓')} {accident_severity.get(fila[15],'Desconocido')}",
                    "KNN": f"{severity_emojis.get(fila[16],'❓')} {accident_severity.get(fila[16],'Desconocido')}",
                    "SVM": f"{severity_emojis.get(fila[17],'❓')} {accident_severity.get(fila[17],'Desconocido')}",
                    "fecha_prediccion": str(fila[18])
                }
            })
        
        historial_data = {"id_usuario": id_usuario, "historial": historial}
        
        # Generar PDF
        pdf_buffer = generar_pdf_historial(historial_data, nombre_usuario)
        
        # Crear y enviar email
        msg = Message(
            subject=f"Historial de Predicciones - {nombre_usuario}",
            recipients=[email_destino],
            body=f"""Hola {nombre_usuario},

Adjunto encontrarás tu historial completo de predicciones de severidad de accidentes.

Este documento contiene todas las predicciones que has realizado en el sistema, incluyendo:
- Datos ingresados para cada análisis
- Resultados de los tres modelos de predicción (Random Forest, KNN, SVM)
- Fechas y horas de cada predicción

Total de predicciones: {len(historial)}

Gracias por usar nuestro Sistema de Predicción de Severidad de Accidentes.

---
Este es un correo automático, por favor no responder.
"""
        )
        
        # Adjuntar PDF
        msg.attach(
            f"historial_{nombre_usuario}.pdf",
            "application/pdf",
            pdf_buffer.read()
        )
        
        # Enviar email
        mail.send(msg)
        
        return jsonify({
            "mensaje": "Historial enviado exitosamente",
            "email": email_destino,
            "total_predicciones": len(historial)
        }), 200
        
    except Exception as e:
        print(f"Error al enviar historial: {str(e)}")
        return jsonify({"error": f"Error al enviar el correo: {str(e)}"}), 500