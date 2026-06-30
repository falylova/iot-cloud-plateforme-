```markdown
<div align="center">

# 🌱 Plateforme IoT Cloud — Surveillance Agricole

**Projet universitaire** · M2 Électronique · ESPA Antananarivo

`Cloud Computing` · `2025-2026`

Réalisé par **FANANTENANA Faly Lovasoa**

[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![MQTT](https://img.shields.io/badge/MQTT-Mosquitto-3C5280?logo=eclipsemosquitto&logoColor=white)](https://mosquitto.org/)
[![InfluxDB](https://img.shields.io/badge/InfluxDB-2.7-22ADF6?logo=influxdb&logoColor=white)](https://www.influxdata.com/)
[![Grafana](https://img.shields.io/badge/Grafana-Dashboard-F46800?logo=grafana&logoColor=white)](https://grafana.com/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)

</div>

---

## 📖 Description

Plateforme IoT **cloud-ready** permettant de collecter, stocker et visualiser **en temps réel** les données de capteurs agricoles simulés.

| Composant | Rôle |
|---|---|
| 🛰️ **MQTT / Mosquitto** | Communication légère entre capteurs et service cloud |
| 🐍 **Python (paho-mqtt)** | Simulation des capteurs et bridge MQTT → InfluxDB |
| 🗄️ **InfluxDB 2.7** | Stockage des séries temporelles |
| 📊 **Grafana** | Visualisation en temps réel via dashboard préconfiguré |
| 🐳 **Docker Compose** | Orchestration de l'ensemble des services |

> ✨ Le dashboard Grafana est **provisionné automatiquement** au démarrage : aucune configuration manuelle n'est nécessaire pour visualiser les données.

---

## 🏗️ Architecture

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

## 📁 Structure du projet

```
iot_cloud_complete/
├── docker-compose.yml              # Orchestration des services
├── simulator/
│   └── sensor_simulator.py         # Simulateur de capteurs agricoles
├── cloud-service/
│   ├── app.py                      # Bridge MQTT → InfluxDB
│   ├── requirements.txt            # Dépendances Python
│   └── Dockerfile                  # Image Docker du service cloud
├── mosquitto/
│   └── mosquitto.conf              # Configuration du broker MQTT
└── grafana/
    └── provisioning/
        ├── datasources/
        │   └── influxdb.yml        # Connexion automatique à InfluxDB
        └── dashboards/
            ├── dashboard.yml       # Déclaration du dossier de dashboards
            └── iot-dashboard.json  # Dashboard préconfiguré
```

---

## ⚙️ Prérequis

- [Docker](https://docs.docker.com/get-docker/) installé
- [Python 3.x](https://www.python.org/downloads/) installé (pour le simulateur)
- `paho-mqtt` installé localement :
  ```bash
  pip install paho-mqtt
  ```

---

## 🚀 Lancement

### 1️⃣ Cloner le dépôt

```bash
git clone https://github.com/falylova/iot-cloud-plateforme.git
cd iot-cloud-plateforme
```

### 2️⃣ Démarrer les services Docker

```bash
# Premier lancement (build inclus)
docker compose -p iot up -d --build

# Lancements suivants
docker compose -p iot up -d
```

> ⏳ **Important** — Grafana peut mettre **entre 1 et 5 minutes** avant d'être pleinement opérationnel (migrations de base de données, chargement des plugins, provisioning des datasources et du dashboard). C'est normal, contrairement à InfluxDB qui démarre presque instantanément. Patientez avant de conclure que la connexion ne fonctionne pas.
>
> Suivre le démarrage en temps réel :
> ```bash
> docker compose -p iot logs -f grafana
> ```
> Grafana est prêt lorsque le log affiche : `msg="HTTP Server Listen" address=[::]:3000`

### 3️⃣ Lancer le simulateur de capteurs

```bash
python3 simulator/sensor_simulator.py
```

### 4️⃣ Accéder aux interfaces

| Service | URL | Identifiants |
|---|---|---|
| 🗄️ InfluxDB | http://localhost:8086 | `admin` / `admin12345` |
| 📊 Grafana | http://localhost:3000 | `admin` / `admin` |

Le dashboard **« IoT Dashboards »** est disponible une fois Grafana démarré, déjà connecté à InfluxDB — aucune configuration manuelle requise.

---

## 🛑 Arrêter la plateforme

```bash
docker compose -p iot down
```

---

## 🔧 Résolution de problèmes

<details>
<summary><b>Grafana met longtemps à démarrer ou semble ne pas se connecter</b></summary>

Patientez jusqu'à 5 minutes au premier lancement, puis vérifiez l'état avec :
```bash
docker compose -p iot logs -f grafana
```
</details>

<details>
<summary><b>InfluxDB ne reçoit plus de données après une mise en veille</b></summary>

```bash
docker restart iot-cloud-service-1
```
</details>

<details>
<summary><b>Voir les logs du service cloud</b></summary>

```bash
docker compose -p iot logs -f cloud-service
```
</details>

<details>
<summary><b>Vérifier que MQTT reçoit les données</b></summary>

```bash
docker exec iot-mosquitto-1 mosquitto_sub -t "iot/sensors" -v
```
</details>

<details>
<summary><b>Le dashboard Grafana n'affiche pas de données (datasource non connectée)</b></summary>

Vérifier que l'UID de la datasource dans `grafana/provisioning/datasources/influxdb.yml` correspond bien à celui référencé dans `grafana/provisioning/dashboards/iot-dashboard.json` :
```bash
grep -o '"uid": *"[^"]*"' grafana/provisioning/dashboards/iot-dashboard.json | sort -u
```
</details>

---

<div align="center">

*Projet réalisé dans le cadre du module Cloud Computing — ESPA Antananarivo*

</div>
```
