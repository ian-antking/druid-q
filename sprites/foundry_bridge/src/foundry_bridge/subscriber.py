import json
import paho.mqtt.client as mqtt
from events import EventValidator
from .strings import MESSAGES

class Subscriber:
    def __init__(self, host, username, password, topic, queue, validator: EventValidator):
        ws_path = "/ws"

        self.topic = topic
        self.queue = queue
        self.validator = validator

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
            print("Received non-JSON payload")
            return 

        if self.validator.run(payload):
            event_obj = self.validator.parse(payload) if hasattr(self.validator, "parse") else payload
            self.queue.put(event_obj)
        else:
            print(f"Invalid message payload on topic {msg.topic}: {payload}")

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()
