import queue
from smartcard.System import readers
from smartcard.CardMonitoring import CardMonitor
from observer import NFCCardObserver
from publisher import Publisher
from screen import ScreenManager
from event import InfoEvent, GameEvent
from dotenv import load_dotenv
import os

from strings import MESSAGES

load_dotenv()

DRUID_URL = os.getenv("DRUID_URL")
DRUID_USERNAME = os.getenv("DRUID_USERNAME")
DRUID_PASSWORD = os.getenv("DRUID_PASSWORD")

if not (DRUID_URL and DRUID_USERNAME and DRUID_PASSWORD):
    raise EnvironmentError(MESSAGES["missing_env_error"])

def main():
    r = readers()
    screen = ScreenManager()
    if not r:
        screen.update(InfoEvent(MESSAGES["no_reader"]))
        return

    screen.update(InfoEvent(MESSAGES["available_readers"].format(readers=r)))

    card_monitor = CardMonitor()
    event_queue = queue.Queue()
    observer = NFCCardObserver(event_queue=event_queue)
    card_monitor.addObserver(observer)

    publisher = Publisher(DRUID_URL, DRUID_USERNAME, DRUID_PASSWORD)

    try:
        while True:
            try:
                event = event_queue.get(timeout=1)

                if isinstance(event, GameEvent):
                    publisher.publish(event.payload)
                    screen.update(InfoEvent(MESSAGES["published_event"].format(event=event.payload)))
                else:
                    screen.update(event.payload)

            except queue.Empty:
                pass

    except KeyboardInterrupt:
        screen.update(InfoEvent(MESSAGES["user_interrupt"]))
    finally:
        card_monitor.deleteObserver(observer)
        publisher.close()

if __name__ == "__main__":
    main()
