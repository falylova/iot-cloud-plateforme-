import random
import time
import json
import paho.mqtt.publish as publish
from datetime import datetime

# ==================== PARAMÈTRES DE BASE ====================
base_values = {
    "temperature": 24.5,
    "humidity": 58.0,
    "soil_moisture": 62.0,
    "light": 680
}

print("Simulateur IoT Agricole démarré")

while True:
    current_hour = datetime.now().hour
    now = datetime.now()

    # ===================== SIMULATION RÉALISTE =====================

    # 1. Cycle jour/nuit pour la luminosité
    if 6 <= current_hour <= 18:
        target_light = random.uniform(750, 1150)
    else:
        target_light = random.uniform(0, 120)

    # 2. Influence de la température sur l'humidité (plus chaud = air plus sec)
    temp_influence = (base_values["temperature"] - 25) * 0.6   # Plus chaud → humidité baisse

    # 3. Mise à jour progressive des valeurs
    for key in base_values:
        # Bruit sensor naturel (petites fluctuations)
        noise = random.uniform(-0.7, 0.7)
        
        if key == "temperature":
            change = random.uniform(-0.4, 0.5) + noise
            base_values[key] += change
            base_values[key] = max(18.0, min(36.0, base_values[key]))
            
        elif key == "humidity":
            change = random.uniform(-0.6, 0.6) - temp_influence * 0.03 + noise
            base_values[key] += change
            base_values[key] = max(35, min(92, base_values[key]))
            
        elif key == "soil_moisture":
            # Séchage naturel
            change = random.uniform(-0.8, -0.1) + noise * 0.5
            base_values[key] += change
            
            # ===================== IRRIGATION AUTOMATIQUE =====================
            if base_values["soil_moisture"] < 38:          # Seuil critique
                print(f"💧 Irrigation activée à {now.strftime('%H:%M:%S')} !")
                base_values["soil_moisture"] += random.uniform(18, 28) 
            
            base_values[key] = max(20, min(85, base_values[key]))
            
        elif key == "light":
            # Transition douce vers la cible jour/nuit
            base_values[key] = base_values[key] * 0.65 + target_light * 0.35
            base_values[key] += noise * 15
            base_values[key] = max(0, min(1200, base_values[key]))

    # ===================== CRÉATION DU PAYLOAD =====================
    payload = {
        "temperature": round(base_values["temperature"], 2),
        "humidity": round(base_values["humidity"], 1),
        "soil_moisture": round(base_values["soil_moisture"], 1),
        "light": round(base_values["light"], 0)
    }
    
    # Envoi via MQTT
    publish.single("iot/sensors", json.dumps(payload), hostname="localhost")
    
    # Affichage console
    print(f"📡 {now.strftime('%H:%M:%S')} → Temp:{payload['temperature']}°C | "
          f"Hum:{payload['humidity']}% | Sol:{payload['soil_moisture']}% | "
          f"Lum:{payload['light']} lux")

    time.sleep(5)
