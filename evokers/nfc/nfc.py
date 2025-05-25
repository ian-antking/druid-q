import queue
from smartcard.System import readers
from smartcard.CardMonitoring import CardMonitor
from observer import NFCCardObserver
from publisher import Publisher
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
    if not r:
        print("❌ No smart card readers found.")
        return

    print("✅ Available readers:", r)
    print("📡 Waiting for cards...")

    card_monitor = CardMonitor()
    data_queue = queue.Queue()
    observer = NFCCardObserver(data_queue=data_queue)
    card_monitor.addObserver(observer)

    publisher = Publisher(DRUID_URL, DRUID_USERNAME, DRUID_PASSWORD)

    try:
        while True:
            try:
                data = data_queue.get(timeout=1)
                print("🚀 Main received JSON object from card:")
                print(data)
                publisher.publish(data['topic'], data['message'])
            except queue.Empty:
                pass
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user.")
    finally:
        card_monitor.deleteObserver(observer)
        publisher.close()

if __name__ == "__main__":
    main()
