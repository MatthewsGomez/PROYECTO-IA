from flask import Blueprint, request, jsonify
import joblib
import pandas as pd
from datetime import datetime
from config.db_config import init_db
from mappings import accident_severity, day_of_week, junction_control, junction_detail, light_conditions, local_authority, road_surface_conditions, road_type, speed_limit, urban_or_rural_area, weather_conditions, vehicle_type, number_of_casualties, number_of_vehicles

predict_bp = Blueprint('predict_routes', __name__)
mysql = None

# Cargar los modelos
rf = joblib.load("modelos/modelo_random_forest.pkl")
svm = joblib.load("modelos/modelo_svm.pkl")
knn = joblib.load("modelos/modelo_knn.pkl")
scaler = joblib.load("modelos/escalador.pkl")

# Emojis para severidad
severity_emojis = {0: "💚", 1: "🚑", 2: "🚨"}

# Ruta principal
@predict_bp.route("/", methods=["GET"])
def home():
    return jsonify({"mensaje": "✅ API de predicción de accidentes funcionando"})

# Ruta de predicción
@predict_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    id_usuario = data.get("id_usuario", None)

    columnas = [
        'Day_of_Week', 'Junction_Control', 'Junction_Detail', 'Light_Conditions',
        'Local_Authority_(District)', 'Road_Surface_Conditions', 'Road_Type',
        'Speed_limit', 'Urban_or_Rural_Area', 'Weather_Conditions',
        'Vehicle_Type', 'Number_of_Casualties', 'Number_of_Vehicles'
    ]

    nuevo = pd.DataFrame([data], columns=columnas)
    nuevo_scaled = scaler.transform(nuevo)

    pred_rf = rf.predict(nuevo_scaled)[0]
    pred_svm = svm.predict(nuevo_scaled)[0]
    pred_knn = knn.predict(nuevo_scaled)[0]

    cursor = mysql.connection.cursor()

    cursor.execute("""
        INSERT INTO respuestas (
            id_usuario, Day_of_Week, Junction_Control, Junction_Detail, Light_Conditions,
            Local_Authority_District, Road_Surface_Conditions, Road_Type, Speed_limit,
            Urban_or_Rural_Area, Weather_Conditions, Vehicle_Type, 
            Number_of_Casualties, Number_of_Vehicles, fecha_respuesta
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """, (
        id_usuario,
        data['Day_of_Week'], data['Junction_Control'], data['Junction_Detail'],
        data['Light_Conditions'], data['Local_Authority_(District)'],
        data['Road_Surface_Conditions'], data['Road_Type'], data['Speed_limit'],
        data['Urban_or_Rural_Area'], data['Weather_Conditions'], data['Vehicle_Type'],
        data['Number_of_Casualties'], data['Number_of_Vehicles']
    ))

    id_respuesta = cursor.lastrowid

    cursor.execute("""
        INSERT INTO predicciones (
            id_respuestas, modelo_RF, modelo_KNN, modelo_SVM, fecha_prediccion
        ) VALUES (%s, %s, %s, %s, NOW())
    """, (id_respuesta, int(pred_rf), int(pred_knn), int(pred_svm)))

    mysql.connection.commit()
    cursor.close()

    resultados = {
        "RandomForest": f"{severity_emojis.get(pred_rf,'❓')} {accident_severity.get(pred_rf, 'Desconocido')}",
        "SVM": f"{severity_emojis.get(pred_svm,'❓')} {accident_severity.get(pred_svm, 'Desconocido')}",
        "KNN": f"{severity_emojis.get(pred_knn,'❓')} {accident_severity.get(pred_knn, 'Desconocido')}",
        "MejorModelo": "Random Forest (93.5% accuracy)",
        "Guardado": f"✅ Registro guardado con ID {id_respuesta}",
        "datos_ingresados": {
            "Day_of_Week": day_of_week.get(data['Day_of_Week'], data['Day_of_Week']),
            "Junction_Control": junction_control.get(data['Junction_Control'], data['Junction_Control']),
            "Junction_Detail": junction_detail.get(data['Junction_Detail'], data['Junction_Detail']),
            "Light_Conditions": light_conditions.get(data['Light_Conditions'], data['Light_Conditions']),
            "Local_Authority_District": local_authority.get(data['Local_Authority_(District)'], data['Local_Authority_(District)']),
            "Road_Surface_Conditions": road_surface_conditions.get(data['Road_Surface_Conditions'], data['Road_Surface_Conditions']),
            "Road_Type": road_type.get(data['Road_Type'], data['Road_Type']),
            "Speed_limit": speed_limit.get(data['Speed_limit'], data['Speed_limit']),
            "Urban_or_Rural_Area": urban_or_rural_area.get(data['Urban_or_Rural_Area'], data['Urban_or_Rural_Area']),
            "Weather_Conditions": weather_conditions.get(data['Weather_Conditions'], data['Weather_Conditions']),
            "Vehicle_Type": vehicle_type.get(data['Vehicle_Type'], data['Vehicle_Type']),
            "Number_of_Casualties": number_of_casualties.get(data['Number_of_Casualties'], data['Number_of_Casualties']),
            "Number_of_Vehicles": number_of_vehicles.get(data['Number_of_Vehicles'], data['Number_of_Vehicles']),
        }
    }

    return jsonify(resultados)
