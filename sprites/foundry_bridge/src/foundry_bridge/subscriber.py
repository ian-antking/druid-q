import json
import paho.mqtt.client as mqtt
from .strings import MESSAGES

class Subscriber:
    def __init__(self, host, username, password, topic, queue):
        ws_path = "/ws"

        self.topic = topic
        self.queue = queue

        self.client = mqtt.Client(transport="websockets")
        self.client.username_pw_set(username, password)
        self.client.ws_set_options(path=ws_path)
        self.client.tls_set()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        self.client.connect(host, 443)
        self.client.loop_start()

    def _on_connect(self, client, _, __, rc):
        if rc == 0:
            client.subscribe(self.topic)
        else:
            print(MESSAGES["connection_failed".format(code=rc)])

    def _on_message(self, _, __, msg):
        try:
            payload = json.loads(msg.payload.decode())
        except json.JSONDecodeError:
            payload = msg.payload.decode()

        self.queue.put({
            "topic": msg.topic,
            "message": payload
        })

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()
