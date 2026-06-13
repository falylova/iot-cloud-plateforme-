import json
from paho.mqtt import client as mqtt
from influxdb_client import InfluxDBClient, Point

# Configuration InfluxDB
token = 'mytoken123'
org = 'university'
bucket = 'sensors'

client_db = InfluxDBClient(url='http://influxdb:8086', token=token, org=org)
write_api = client_db.write_api()

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        
        # Création du point InfluxDB avec tous les capteurs
        point = (Point("environment")
                 .field("temperature", float(data["temperature"]))
                 .field("humidity", float(data["humidity"]))
                 .field("soil_moisture", float(data.get("soil_moisture", 50)))
                 .field("light", float(data.get("light", 800))))
        
        write_api.write(bucket=bucket, org=org, record=point)
        print("✅ Données sauvegardées :", data)
        
    except Exception as e:
        print("❌ Erreur lors du traitement du message :", e)

# Configuration MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect("mosquitto", 1883, 60)
client.subscribe("iot/sensors")

print("🚀 Service Cloud IoT démarré - En attente de données...")
client.loop_forever()
