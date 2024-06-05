import paho.mqtt.client as mqtt
import time
import json
import random

BROKER_ADDRESS = "mqtt"
BROKER_PORT = 1883
TOPIC = "iot/data"

client = mqtt.Client()
client.connect(BROKER_ADDRESS, BROKER_PORT, 60)

while True:
    payload = json.dumps({
        "device_id": "device1",
        "temperature": random.uniform(20.0, 30.0),
        "humidity": random.uniform(30.0, 50.0),
        "timestamp": int(time.time())
    })
    client.publish(TOPIC, payload)
    print(f"Published: {payload}")
    time.sleep(5)
