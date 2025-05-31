import argparse
import queue
import os
import paho.mqtt.client as mqtt
from smartcard.CardMonitoring import CardMonitor
from dotenv import load_dotenv
from .observer import NFCCardObserver
from publisher import Publisher
from .screen import TerminalScreen
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
    args = parser.parse_args()

    if args.display_hat:
        raise NotImplementedError("Display Hat support is not implemented yet.")
    else:
        screen = TerminalScreen()

    event_queue = queue.Queue()
    observer = NFCCardObserver(event_queue=event_queue)
    monitor = CardMonitor()
    
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
