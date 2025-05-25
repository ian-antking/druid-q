import queue
from smartcard.System import readers
from smartcard.CardMonitoring import CardMonitor
from observer import NFCCardObserver
from publisher import Publisher
from screen import ScreenManager
from dotenv import load_dotenv
import os

load_dotenv()

DRUID_URL = os.getenv("DRUID_URL")
DRUID_USERNAME = os.getenv("DRUID_USERNAME")
DRUID_PASSWORD = os.getenv("DRUID_PASSWORD")

if not (DRUID_URL and DRUID_USERNAME and DRUID_PASSWORD):
    raise EnvironmentError("Missing one or more Druid environment variables.")

def main():
    r = readers()
    screen = ScreenManager()  # Starts internal thread

    if not r:
        screen.update({"type": "info", "message": "❌ No smart card readers found."})
        return

    screen.update({
        "type": "info",
        "message": f"✅ Available readers: {r}\n📡 Waiting for cards..."
    })

    card_monitor = CardMonitor()
    event_queue = queue.Queue()
    observer = NFCCardObserver(event_queue=event_queue)
    card_monitor.addObserver(observer)

    publisher = Publisher(DRUID_URL, DRUID_USERNAME, DRUID_PASSWORD)

    try:
        while True:
            try:
                event = event_queue.get(timeout=1)

                if event.type == "game":
                    publisher.publish(event.payload['topic'], event.payload['message'])
                    screen.update({
                        "type": "info",
                        "message": f"🚀 Published game event: {event.payload}"
                    })
                else:
                    screen.update(event.payload)

            except queue.Empty:
                pass

    except KeyboardInterrupt:
        screen.update({"type": "info", "message": "🛑 Interrupted by user."})
    finally:
        card_monitor.deleteObserver(observer)
        publisher.close()

if __name__ == "__main__":
    main()
