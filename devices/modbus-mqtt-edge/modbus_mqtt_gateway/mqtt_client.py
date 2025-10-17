import random
from paho.mqtt import client as mqtt_client

broker = 'localhost'
port = 1883
username = 'user1'
password = 'test123'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1)
    #client._callback_api_version = 1   # fix for Python 3.12 + Paho 2.x
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    return client

def publish(client, payload, topic):
    result = client.publish(topic, payload)
    if result.rc == 0:
        print(f"Sent `{payload}` to topic `{topic}`")
    else:
        print(f"Failed to send `{payload}` to topic `{topic}`")
