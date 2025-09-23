import os
from dotenv import load_dotenv
from .app import App
from redis import Redis
from .scene_queue import SceneQueue
from .strings import MESSAGES
from .hue import Hue, discover_bridge_ip

load_dotenv()

HUE_API_KEY = os.getenv("HUE_API_KEY")
ROOM_NAME = os.getenv("ROOM_NAME")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = 6379

if not all([HUE_API_KEY, ROOM_NAME]):
    raise EnvironmentError(MESSAGES["missing_env_error"])

def main() :
    print(HUE_API_KEY)
    print(ROOM_NAME)
    print(REDIS_HOST)

    redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    cache = SceneQueue(redis_client)

    bridge_ip = cache.get_hue_ip()

    if bridge_ip is None:
        bridge_ip = discover_bridge_ip()
        cache.set_hue_ip(bridge_ip)

    hue = Hue(bridge_ip)

    app = App(cache, hue)

    app.run()

if __name__ == "__main__":
    main()
