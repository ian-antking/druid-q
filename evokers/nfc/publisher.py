import json
import paho.mqtt.client as mqtt
from urllib.parse import urlparse


class Publisher:
    def __init__(self, host, username, password):
        ws_path = "/ws"

        print(f"Connecting to host: {host} with WS path: {ws_path}")

        self.client = mqtt.Client(transport="websockets")
        self.client.username_pw_set(username, password)
        self.client.ws_set_options(path=ws_path)
        self.client.tls_set()
        self.client.connect(host, 443)
        self.client.loop_start()

    def publish(self, event):
        payload = json.dumps(event["message"])
        self.client.publish(event["topic"], payload)

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()
