import queue
from smartcard.System import readers
from smartcard.CardMonitoring import CardMonitor
from observer import NFCCardObserver
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

    try:
        while True:
            try:
                data = data_queue.get(timeout=1)
                print("🚀 Main received JSON object from card:")
                print(data)
            except queue.Empty:
                pass
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user.")
    finally:
        card_monitor.deleteObserver(observer)

if __name__ == "__main__":
    main()
