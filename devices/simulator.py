import asyncio
import json
import random
from datetime import datetime
import paho.mqtt.client as mqtt
import sys

BROKER = "localhost"      # MQTT broker address
PORT = 1883
NUM_DEVICES = 5           # Number of simulated machines
PUBLISH_INTERVAL = 2      # seconds
TOPIC_PREFIX = "factory/machines"

# Authentication credentials
USERNAME = "user1"
PASSWORD = "test123"

# --- Callbacks ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker")
    else:
        print(f"❌ Failed to connect, return code {rc}")
        sys.exit(1)

def on_publish(client, userdata, mid):
    print(f"📤 Message published successfully (mid: {mid})")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("⚠️ Unexpected disconnection from broker")

# --- Create MQTT client ---
client = mqtt.Client(client_id="simulator", protocol=mqtt.MQTTv311)
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect

# --- Connect to broker ---
try:
    client.connect(BROKER, PORT, keepalive=60)
except Exception as e:
    print(f"❌ Could not connect to broker: {e}")
    sys.exit(1)

# Start the network loop in background thread
client.loop_start()

# --- Payload generation ---
def generate_payload(device_id):
    temperature = random.uniform(60, 80)
    vibration = random.uniform(0.1, 0.3)
    pressure = random.uniform(100, 105)

    # Random anomaly
    if random.random() < 0.05:  # 5% chance
        temperature += random.uniform(20, 40)
        vibration += random.uniform(0.5, 1.0)

    status = "running" if temperature < 100 else "fault"

    return {
        "device_id": f"machine-{device_id:02d}",
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": round(temperature, 2),
        "vibration": round(vibration, 3),
        "pressure": round(pressure, 2),
        "status": status
    }

# --- Async publishing ---
async def publish_device(device_id):
    while True:
        payload = generate_payload(device_id)
        topic = f"{TOPIC_PREFIX}/machine-{device_id:02d}"
        result = client.publish(topic, json.dumps(payload), qos=1)

        # Optional: check publish result
        if result.rc != 0:
            print(f"❌ Failed to publish {topic}")
        else:
            print(f"[MQTT] Published {topic}: {payload}")

        await asyncio.sleep(PUBLISH_INTERVAL)

# --- Main async function ---
async def main():
    tasks = [asyncio.create_task(publish_device(i)) for i in range(1, NUM_DEVICES + 1)]
    await asyncio.gather(*tasks)

# --- Entry point ---
if __name__ == "__main__":
    asyncio.run(main())