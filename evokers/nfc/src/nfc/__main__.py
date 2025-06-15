import argparse
from pathlib import Path
import queue
import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

from .observer import ACR122U, PN532
from publisher import Publisher
from .screen import TerminalScreen
from .app import App
from .strings import MESSAGES

from .scene_store import JsonSceneStore

load_dotenv()

DRUID_HOST = os.getenv("DRUID_HOST")
DRUID_USERNAME = os.getenv("DRUID_USERNAME")
DRUID_PASSWORD = os.getenv("DRUID_PASSWORD")

if not (DRUID_HOST and DRUID_USERNAME and DRUID_PASSWORD):
    raise EnvironmentError(MESSAGES["missing_env_error"])

def main():
    parser = argparse.ArgumentParser(description="Run the NFC Scene Controller")
    parser.add_argument("--use-pn532", action="store_true", help="Use PN532 NFC HAT instead of USB ARC122U reader")
    args = parser.parse_args()

    screen = TerminalScreen()
    event_queue = queue.Queue()

    if args.use_pn532:
        observer = PN532(event_queue=event_queue)
    else:
        observer = ACR122U(event_queue=event_queue)

    client = mqtt.Client(protocol=mqtt.MQTTv311, transport="websockets")
    client.username_pw_set(DRUID_USERNAME, DRUID_PASSWORD)
    client.ws_set_options(path="/ws")
    client.tls_set()
    client.connect(DRUID_HOST, 443)

    publisher = Publisher(client)

    BASE_DIR = Path(__file__).resolve().parents[2]
    scene_file = BASE_DIR / "scenes.json"

    scene_store = JsonSceneStore(scene_file)

    app = App(
        screen=screen,
        event_queue=event_queue,
        observer=observer,
        publisher=publisher,
        scene_store=scene_store,
    )

    app.run()

if __name__ == "__main__":
    main()
