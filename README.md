# 🚛 IoT Fleet Tracker — Real-Time Vehicle Monitoring Pipeline

A full-stack IoT data pipeline built on AWS that simulates a fleet of delivery trucks
sending real-time GPS and sensor data to the cloud, processes it with serverless functions,
stores it in a NoSQL database, and displays it on a live web dashboard.

---

## 🏗️ Architecture
```
IoT Devices (Python Simulator)
        │  MQTT over TLS
        ▼
AWS IoT Core  ──► IoT Rule
                      │
                      ▼
              AWS Lambda (Python)
              - Validates payload
              - Detects harsh driving events
              - Saves to database
                      │
                      ▼
              AWS DynamoDB
              - Stores all sensor readings
              - Partition key: vehicle_id
              - Sort key: timestamp
                      │
                      ▼
              EC2 Instance (FastAPI)
              - REST API serves latest vehicle data
              - /vehicles endpoint
              - /vehicles/{id} history endpoint
                      │
                      ▼
              HTML/JS Dashboard
              - Live map (OpenStreetMap + Leaflet.js)
              - Auto-refreshes every 5 seconds
              - Vehicle stats: speed, fuel, engine temp
              - Anomaly alerts
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| IoT Device Simulation | Python, paho-mqtt |
| Message Broker | AWS IoT Core (MQTT over TLS) |
| Serverless Processing | AWS Lambda (Python 3.12) |
| Database | AWS DynamoDB (NoSQL) |
| Backend API | FastAPI on AWS EC2 (t3.micro) |
| Frontend | HTML, CSS, JavaScript, Leaflet.js |
| Security | AWS IAM roles, X.509 certificates, .env secrets |
| Infrastructure | AWS Free Tier |

---

## 🚀 Features

- **Real-time data pipeline** — sensor readings flow from device to dashboard in under 2 seconds
- **3 simulated vehicles** sending GPS coordinates, speed, engine temperature, fuel level, and accelerometer data
- **Anomaly detection** — Lambda function flags harsh braking or collision events using accelerometer magnitude
- **Live map** — trucks move in real time on an OpenStreetMap-powered dashboard
- **REST API** — FastAPI server on EC2 exposes `/vehicles` and `/vehicles/{id}` endpoints
- **Secure by design** — TLS mutual authentication, IAM roles, certificates never committed to git

---

## 📁 Project Structure
```
iot-fleet-tracker/
├── simulator/
│   └── simulator.py          # Simulates IoT devices sending MQTT messages
├── lambda_function/
│   └── lambda_handler.py     # AWS Lambda — processes and stores sensor data
├── ec2_server/
│   ├── main.py               # FastAPI server running on EC2
│   └── requirements.txt
├── dashboard/
│   └── index.html            # Live dashboard (HTML + JS + Leaflet.js)
├── requirements.txt
├── .gitignore                # Excludes certs/ and .env
└── README.md
```

---

## ⚙️ Setup & Running Locally

### Prerequisites
- Python 3.10+
- AWS account (Free Tier)
- AWS CLI configured

### 1. Clone the repo
```bash
git clone https://github.com/KirrozToo/iot-fleet-tracker.git
cd iot-fleet-tracker
```

### 2. Install dependencies
```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

### 3. Configure environment
Create a `.env` file in the root:
```
AWS_IOT_ENDPOINT=your-endpoint.iot.us-east-1.amazonaws.com
CERT_PATH=certs/device-certificate.pem.crt
KEY_PATH=certs/private.pem.key
CA_PATH=certs/AmazonRootCA1.pem
```

### 4. Add your certificates
Place your AWS IoT device certificates in the `certs/` folder:
```
certs/
├── device-certificate.pem.crt
├── private.pem.key
└── AmazonRootCA1.pem
```

### 5. Run the simulator
```bash
python simulator/simulator.py
```

### 6. Open the dashboard
Open `dashboard/index.html` in your browser.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/vehicles` | Latest reading for all vehicles |
| GET | `/vehicles/{vehicle_id}` | Full history for a specific vehicle |

**Base URL:** `http://52.73.235.31:8000`

---

## ☁️ AWS Services Used

- **AWS IoT Core** — MQTT message broker, device registry, IoT rules engine
- **AWS Lambda** — Serverless function triggered on every sensor reading
- **AWS DynamoDB** — NoSQL database storing all time-series sensor data
- **AWS EC2** — Ubuntu instance hosting the FastAPI backend
- **AWS IAM** — Roles and policies securing service-to-service communication

---

## 📌 Relevance to IoT & Edge Computing

This project mirrors real-world logistics IoT architecture where:
- Edge devices (trucks) publish sensor data over MQTT
- Cloud ingestion layer (IoT Core) handles millions of concurrent connections
- Serverless functions process and enrich data at scale
- Time-series data is stored for analytics and alerting
- Operations teams monitor fleets via live dashboards

---

*Built as a hands-on demonstration of AWS IoT infrastructure and real-time data pipelines.*
