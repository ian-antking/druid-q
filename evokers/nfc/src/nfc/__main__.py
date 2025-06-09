import argparse
import queue
import os
import paho.mqtt.client as mqtt
from smartcard.CardMonitoring import CardMonitor
from dotenv import load_dotenv

from .observer import ARC122U, PN532
from publisher import Publisher
from .screen import TerminalScreen, DisplayHatScreen
from .app import App
from .strings import MESSAGES

load_dotenv()

DRUID_HOST = os.getenv("DRUID_HOST")
DRUID_USERNAME = os.getenv("DRUID_USERNAME")
DRUID_PASSWORD = os.getenv("DRUID_PASSWORD")

if not (DRUID_HOST and DRUID_USERNAME and DRUID_PASSWORD):
    raise EnvironmentError(MESSAGES["missing_env_error"])

def main():
    parser = argparse.ArgumentParser(description="Run the NFC Scene Controller")
    parser.add_argument("--display-hat", action="store_true", help="Use Display Hat Mini instead of terminal")
    parser.add_argument("--use-pn532", action="store_true", help="Use PN532 NFC HAT instead of USB ARC122U reader")
    args = parser.parse_args()

    if args.display_hat:
        screen = DisplayHatScreen()
    else:
        screen = TerminalScreen()

    event_queue = queue.Queue()

    if args.use_pn532:
        observer = PN532(event_queue=event_queue)
        monitor = None  # No CardMonitor needed for PN532 polling
    else:
        observer = ARC122U(event_queue=event_queue)
        monitor = CardMonitor()  # USB reader uses CardMonitor

    client = mqtt.Client(transport="websockets")
    client.username_pw_set(DRUID_USERNAME, DRUID_PASSWORD)
    client.ws_set_options(path="/ws")
    client.tls_set()
    client.connect(DRUID_HOST, 443)

    publisher = Publisher(client)

    app = App(screen, event_queue, observer, publisher, monitor)
    app.run()

if __name__ == "__main__":
    main()
