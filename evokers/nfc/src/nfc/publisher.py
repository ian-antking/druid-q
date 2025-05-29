import json
from paho.mqtt.client import Client

class Publisher:
    def __init__(self, client: Client):
        self.client = client
        self.client.loop_start()

    def publish(self, event):
        payload = json.dumps(event["message"])
        self.client.publish(event["topic"], payload)

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()

