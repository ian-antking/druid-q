from smartcard.System import readers
from smartcard.CardMonitoring import CardMonitor
from observer import NFCCardObserver
import time

def main():
    r = readers()
    if not r:
        print("❌ No smart card readers found.")
        return

    print("✅ Available readers:", r)
    print("📡 Waiting for cards...")

    card_monitor = CardMonitor()
    observer = NFCCardObserver()
    card_monitor.addObserver(observer)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user.")
    finally:
        card_monitor.deleteObserver(observer)

if __name__ == "__main__":
    main()
