import json
import time
import random
import ssl
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

load_dotenv()

# ── AWS IoT Core settings (fill these in after Phase 2) ──────────────────────
ENDPOINT   = os.getenv("AWS_IOT_ENDPOINT", "YOUR_ENDPOINT.iot.us-east-1.amazonaws.com")
PORT       = 8883
TOPIC      = "fleet/vehicle/data"
CLIENT_ID  = "truck-simulator-01"

CERT_PATH  = os.getenv("CERT_PATH",  "certs/device-certificate.pem.crt")
KEY_PATH   = os.getenv("KEY_PATH",   "certs/private.pem.key")
CA_PATH    = os.getenv("CA_PATH",    "certs/AmazonRootCA1.pem")


# ── Simulate 3 trucks driving around the San Jose / Bay Area ─────────────────
VEHICLES = [
    {"id": "truck-01", "lat": 37.3382,  "lon": -121.8863},  # San Jose
    {"id": "truck-02", "lat": 37.5485,  "lon": -121.9886},  # Fremont
    {"id": "truck-03", "lat": 37.6879,  "lon": -122.4702},  # San Francisco
]


def move_vehicle(vehicle):
    """Nudge a vehicle's position slightly to simulate driving."""
    vehicle["lat"] += random.uniform(-0.002, 0.002)
    vehicle["lon"] += random.uniform(-0.002, 0.002)
    return vehicle


def generate_payload(vehicle):
    """Build the JSON payload a real IoT sensor would send."""
    return {
        "vehicle_id":   vehicle["id"],
        "timestamp":    datetime.now(timezone.utc).isoformat(),
        "location": {
            "lat": round(vehicle["lat"], 6),
            "lon": round(vehicle["lon"], 6),
        },
        "speed_kmh":        round(random.uniform(0, 90), 1),
        "engine_temp_c":    round(random.uniform(75, 105), 1),
        "fuel_level_pct":   round(random.uniform(10, 100), 1),
        "accelerometer": {
            "x": round(random.uniform(-2.0, 2.0), 3),   # lateral G-force
            "y": round(random.uniform(-2.0, 2.0), 3),   # longitudinal G-force
            "z": round(random.uniform(9.5, 10.0), 3),   # vertical (gravity ≈ 9.8)
        },
        "status": random.choice(["moving", "moving", "moving", "idle", "stopped"]),
    }


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅  Connected to AWS IoT Core")
    else:
        print(f"❌  Connection failed with code {rc}")


def on_publish(client, userdata, mid):
    print(f"   ↑ Message published (mid={mid})")


def run():
    client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)

    # TLS mutual authentication with device certificates
    client.tls_set(
        ca_certs=CA_PATH,
        certfile=CERT_PATH,
        keyfile=KEY_PATH,
        tls_version=ssl.PROTOCOL_TLSv1_2,
    )

    client.on_connect = on_connect
    client.on_publish = on_publish

    print(f"🔌  Connecting to {ENDPOINT}:{PORT} ...")
    client.connect(ENDPOINT, PORT, keepalive=60)
    client.loop_start()

    # Give the connection a moment to establish
    time.sleep(2)

    print(f"🚛  Simulating {len(VEHICLES)} vehicles — sending data every 3 seconds.")
    print("    Press Ctrl+C to stop.\n")

    try:
        while True:
            for vehicle in VEHICLES:
                move_vehicle(vehicle)
                payload = generate_payload(vehicle)
                payload_json = json.dumps(payload)

                result = client.publish(TOPIC, payload_json, qos=1)

                print(
                    f"[{payload['timestamp'][11:19]}] "
                    f"{vehicle['id']} | "
                    f"lat={payload['location']['lat']}  "
                    f"lon={payload['location']['lon']}  "
                    f"speed={payload['speed_kmh']} km/h  "
                    f"status={payload['status']}"
                )

            time.sleep(3)

    except KeyboardInterrupt:
        print("\n🛑  Simulator stopped.")
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    run()
