```markdown
# Plateforme IoT Cloud — Surveillance Agricole

Projet universitaire — M2 Electronique, ESPA Antananarivo  
Matière : Cloud Computing | Année : 2025-2026  
Auteur : **FANANTENANA Faly Lovasoa**

---

## Description

Plateforme IoT cloud-ready permettant de collecter, stocker et visualiser en temps réel les données de capteurs agricoles simulés. La solution s'appuie sur :

- **MQTT / Mosquitto** — communication légère entre capteurs et service cloud
- **Python (paho-mqtt)** — simulation des capteurs et bridge MQTT → InfluxDB
- **InfluxDB 2.7** — stockage des séries temporelles
- **Grafana** — visualisation en temps réel via dashboard préconfiguré
- **Docker Compose** — orchestration de l'ensemble des services

Le dashboard Grafana est **provisionné automatiquement** au démarrage : aucune configuration manuelle n'est nécessaire pour visualiser les données.

---

## Architecture

```
Simulator (local)
      │  publish MQTT
      ▼
 Mosquitto :1883
      │  subscribe
      ▼
 Cloud Service (Python)
      │  write()
      ▼
 InfluxDB :8086
      │  Flux query
      ▼
 Grafana :3000
```

---

## Structure du projet

```
iot_cloud_complete/
├── docker-compose.yml          # Orchestration des services
├── simulator/
│   └── sensor_simulator.py     # Simulateur de capteurs agricoles
├── cloud-service/
│   ├── app.py                  # Bridge MQTT → InfluxDB
│   ├── requirements.txt        # Dépendances Python
│   └── Dockerfile              # Image Docker du service cloud
├── mosquitto/
│   └── mosquitto.conf          # Configuration du broker MQTT
└── grafana/
    └── provisioning/
        ├── datasources/
        │   └── influxdb.yml    # Connexion automatique à InfluxDB
        └── dashboards/
            ├── dashboard.yml   # Déclaration du dossier de dashboards
            └── iot-dashboard.json  # Dashboard préconfiguré
```

---

## Prérequis

- [Docker](https://docs.docker.com/get-docker/) installé
- [Python 3.x](https://www.python.org/downloads/) installé (pour le simulateur)
- `paho-mqtt` installé localement : `pip install paho-mqtt`

---

## Lancement

### 1. Cloner le dépôt

```bash
git clone https://github.com/falylova/iot-cloud-plateforme.git
cd iot-cloud-plateforme
```

### 2. Démarrer les services Docker

```bash
# Premier lancement (build inclus)
docker compose -p iot up -d --build

# Lancements suivants
docker compose -p iot up -d
```

> ⏳ **Important :** Grafana peut mettre **entre 1 et 5 minutes** avant d'être pleinement opérationnel (migrations de base de données, chargement des plugins, provisioning des datasources et du dashboard). C'est normal, contrairement à InfluxDB qui démarre presque instantanément. Patientez avant de juger que la connexion ne fonctionne pas.
>
> Pour suivre le démarrage en temps réel :
> ```bash
> docker compose -p iot logs -f grafana
> ```
> Grafana est prêt lorsque le log affiche : `msg="HTTP Server Listen" address=[::]:3000`

### 3. Lancer le simulateur de capteurs

```bash
python3 simulator/sensor_simulator.py
```

### 4. Accéder aux interfaces

| Service  | URL                   | Identifiants       |
|----------|-----------------------|--------------------|
| InfluxDB | http://localhost:8086 | admin / admin12345 |
| Grafana  | http://localhost:3000 | admin / admin      |

Le dashboard Grafana **« IoT Dashboards »** est disponible une fois Grafana démarré, déjà connecté à InfluxDB — aucune configuration manuelle requise.

---

## Arrêter la plateforme

```bash
docker compose -p iot down
```

---

## Résolution de problèmes

**Grafana met longtemps à démarrer ou semble ne pas se connecter :**
Patientez jusqu'à 5 minutes au premier lancement, puis vérifiez l'état avec :
```bash
docker compose -p iot logs -f grafana
```

**InfluxDB ne reçoit plus de données après une mise en veille :**
```bash
docker restart iot-cloud-service-1
```

**Voir les logs du service cloud :**
```bash
docker compose -p iot logs -f cloud-service
```

**Vérifier que MQTT reçoit les données :**
```bash
docker exec iot-mosquitto-1 mosquitto_sub -t "iot/sensors" -v
```

**Le dashboard Grafana n'affiche pas de données (datasource non connectée) :**
Vérifier que l'UID de la datasource dans `grafana/provisioning/datasources/influxdb.yml` correspond bien à celui référencé dans `grafana/provisioning/dashboards/iot-dashboard.json` :
```bash
grep -o '"uid": *"[^"]*"' grafana/provisioning/dashboards/iot-dashboard.json | sort -u
```
```
