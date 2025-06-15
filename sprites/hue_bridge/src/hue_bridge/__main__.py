import queue
import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from events import SceneChangeEventValidator
from subscriber import Subscriber
from .strings import MESSAGES
from .app import App 

load_dotenv()

DRUID_HOST = os.getenv("DRUID_HOST")
DRUID_PORT = int(os.getenv("DRUID_PORT", 443))  # Defaults to 443
DRUID_USERNAME = os.getenv("DRUID_USERNAME")
DRUID_PASSWORD = os.getenv("DRUID_PASSWORD")
DRUID_TOPIC = os.getenv("DRUID_TOPIC")

if not (DRUID_HOST and DRUID_USERNAME and DRUID_PASSWORD and DRUID_TOPIC):
    raise EnvironmentError(MESSAGES["missing_env_error"])

def main():
    q = queue.Queue()

    client = mqtt.Client(transport="websockets")
    client.username_pw_set(DRUID_USERNAME, DRUID_PASSWORD)
    client.ws_set_options(path="/ws")

    if DRUID_PORT == 443:
        client.tls_set()  

    client.connect(DRUID_HOST, DRUID_PORT)

    subscriber = Subscriber(client, DRUID_TOPIC, q, SceneChangeEventValidator())
    app = App(queue=q, subscriber=subscriber)
    app.run()

if __name__ == "__main__":
    main()
