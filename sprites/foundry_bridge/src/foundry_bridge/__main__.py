import queue
import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from events import SceneChangeEventValidator
from subscriber import Subscriber
from .keyboard import KeyboardManager
from .scene_map import SCENE_MAP
from .strings import MESSAGES
from .app import App 

load_dotenv()

DRUID_HOST = os.getenv("DRUID_HOST")
DRUID_USERNAME = os.getenv("DRUID_USERNAME")
DRUID_PASSWORD = os.getenv("DRUID_PASSWORD")
DRUID_TOPIC = os.getenv("DRUID_TOPIC")

if not (DRUID_HOST and DRUID_USERNAME and DRUID_PASSWORD and DRUID_TOPIC):
    raise EnvironmentError(MESSAGES["missing_env_error"])

def main():
    q = queue.Queue()

    client = mqtt.Client(protocol=mqtt.MQTTv311, transport="websockets")
    client.username_pw_set(DRUID_USERNAME, DRUID_PASSWORD)
    client.ws_set_options(path="/ws")
    client.tls_set()
    client.connect(DRUID_HOST, 443)

    subscriber = Subscriber(client, DRUID_TOPIC, q, SceneChangeEventValidator())
    keyboard = KeyboardManager(SCENE_MAP)

    app = App(queue=q, subscriber=subscriber, keyboard_manager=keyboard)
    app.run()

if __name__ == "__main__":
    main()
