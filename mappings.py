# mapping.py

# Severidad del accidente
accident_severity = {
    0: "Serio 🚨 (accidente grave con fallecidos)",
    1: "Grave 🚑 (accidente con heridos graves)",
    2: "Normal 💚 (accidente leve sin heridos)",
}

# Día de la semana
day_of_week = {
    0: "Domingo",
    1: "Lunes",
    2: "Martes",
    3: "Miércoles",
    4: "Jueves",
    5: "Viernes",
    6: "Sábado"
}

# Control de cruce
junction_control = {
    0: "Sin control",
    1: "Señales de stop",
    2: "Semáforo",
    3: "Rotonda",
    4: "Semáforo con sensor",
    5: "Señales de prioridad",
    6: "Otro control"
}

# Detalle del cruce
junction_detail = {
    0: "Cruce simple",
    1: "Cruce en T",
    2: "Cruce en Y",
    3: "Cruce múltiple",
    4: "Rotonda",
    5: "Entrada/salida privada",
    6: "Otro"
}

# Condiciones de luz
light_conditions = {
    0: "Plena luz del día",
    1: "Oscuro sin iluminación",
    2: "Oscuro con iluminación",
    3: "Amanecer/Atardecer",
    4: "Niebla o humo",
    5: "Otro"
}

# Autoridad local (distritos)
local_authority = {
    0: "Distrito 0",
    1: "Distrito 1",
    3: "Distrito 3",
    4: "Distrito 4",
    76: "Distrito 76",
    159: "Distrito 159",
    176: "Distrito 176",
    267: "Distrito 267",
    384: "Distrito 384"
    # Puedes agregar más según existan en tus datos
}

# Condiciones de la superficie de la vía
road_surface_conditions = {
    0: "Asfalto seco",
    1: "Asfalto húmedo",
    2: "Hielo o nieve",
    3: "Grava",
    4: "Otro"
}

# Tipo de vía
road_type = {
    0: "Calle",
    1: "Avenida",
    2: "Carretera principal",
    3: "Carretera secundaria",
    4: "Rotonda",
    5: "Otro"
}

# Límite de velocidad
speed_limit = {
    30: "30 km/h",
    40: "40 km/h",
    50: "50 km/h",
    60: "60 km/h",
    70: "70 km/h",
    80: "80 km/h",
    90: "90 km/h",
    100: "100 km/h",
    110: "110 km/h",
    120: "120 km/h"
}

# Área urbana o rural
urban_or_rural_area = {
    0: "Urbano",
    1: "Rural"
}

# Condiciones climáticas
weather_conditions = {
    0: "Despejado",
    1: "Lluvia ligera",
    2: "Lluvia intensa",
    3: "Niebla",
    4: "Nieve",
    5: "Viento fuerte",
    6: "Otro"
}

# Tipo de vehículo
vehicle_type = {
    0: "Coche",
    1: "Motocicleta",
    2: "Camión",
    3: "Autobús",
    4: "Bicicleta",
    5: "Peatón",
    6: "Otro"
}

# Número de víctimas
number_of_casualties = {
    0: "Sin víctimas",
    1: "1 víctima",
    2: "2 víctimas",
    3: "3 víctimas",
    4: "4 víctimas",
    5: "5 víctimas o más"
}

# Número de vehículos involucrados
number_of_vehicles = {
    1: "1 vehículo",
    2: "2 vehículos",
    3: "3 vehículos",
    4: "4 vehículos",
    5: "5 vehículos o más"
}
