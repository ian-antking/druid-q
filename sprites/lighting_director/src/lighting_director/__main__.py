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
from .hue import get_lights_in_room, discover_bridge_ip
from .llm import LLMClient
import json
from pathlib import Path

load_dotenv()

DRUID_HOST = os.getenv("DRUID_HOST")
DRUID_PORT = int(os.getenv("DRUID_PORT", 443))
DRUID_USERNAME = os.getenv("DRUID_USERNAME")
DRUID_PASSWORD = os.getenv("DRUID_PASSWORD")
DRUID_TOPIC = os.getenv("DRUID_TOPIC")
LLM_API_KEY = os.getenv("LLM_API_KEY")
HUE_API_KEY = os.getenv("HUE_API_KEY")
ROOM_NAME = os.getenv("ROOM_NAME")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = 6379

if not all([DRUID_HOST, DRUID_USERNAME, DRUID_PASSWORD, DRUID_TOPIC, LLM_API_KEY, HUE_API_KEY, ROOM_NAME]):
    raise EnvironmentError(MESSAGES["missing_env_error"])

def main():
    q = queue.Queue()

    lighting_context_path = Path(__file__).parent / "lighting_context.txt"

    with open(lighting_context_path, "r", encoding="utf-8") as f:
        lighting_context = f.read()

    client = mqtt.Client(protocol=mqtt.MQTTv311, transport="websockets")
    client.username_pw_set(DRUID_USERNAME, DRUID_PASSWORD)
    client.ws_set_options(path="/ws")

    if DRUID_PORT == 443:
        client.tls_set()

    client.connect(DRUID_HOST, DRUID_PORT)

    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    scene_store = SceneStore(redis_client)

    room_lights = scene_store.get_room_lights()

    if room_lights is None:
        hue_ip = scene_store.get_hue_ip()

        if hue_ip is None:
            hue_ip = discover_bridge_ip()
            scene_store.set_hue_ip(hue_ip)

        room_lights = get_lights_in_room(ROOM_NAME, HUE_API_KEY, hue_ip)
        scene_store.set_room_lights(json.dumps(room_lights))

    llm_client = LLMClient(api_key=LLM_API_KEY, model="gpt-4", lights=room_lights, lighting_context=lighting_context)
 
    subscriber = Subscriber(client, DRUID_TOPIC, q, SceneChangeEventValidator())
    app = App(queue=q, subscriber=subscriber, scene_store=scene_store, llm_client=llm_client)
    app.run()

if __name__ == "__main__":
    main()
