import queue
import os
import paho.mqtt.client as mqtt
import redis
from dotenv import load_dotenv
from events import SceneChangeEventValidator
from subscriber import Subscriber
from .strings import MESSAGES
from .app import App
from .scene_store import SceneStore

load_dotenv()

DRUID_HOST = os.getenv("DRUID_HOST")
DRUID_PORT = int(os.getenv("DRUID_PORT", 443))
DRUID_USERNAME = os.getenv("DRUID_USERNAME")
DRUID_PASSWORD = os.getenv("DRUID_PASSWORD")
DRUID_TOPIC = os.getenv("DRUID_TOPIC")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = 6379

if not all([DRUID_HOST, DRUID_USERNAME, DRUID_PASSWORD, DRUID_TOPIC]):
    raise EnvironmentError(MESSAGES["missing_env_error"])

def main():
    q = queue.Queue()

    client = mqtt.Client(protocol=mqtt.MQTTv311, transport="websockets")
    client.username_pw_set(DRUID_USERNAME, DRUID_PASSWORD)
    client.ws_set_options(path="/ws")

    if DRUID_PORT == 443:
        client.tls_set()

    client.connect(DRUID_HOST, DRUID_PORT)

    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    scene_store = SceneStore(redis_client)

    subscriber = Subscriber(client, DRUID_TOPIC, q, SceneChangeEventValidator())
    app = App(queue=q, subscriber=subscriber, scene_store=scene_store)
    app.run()

if __name__ == "__main__":
    main()
