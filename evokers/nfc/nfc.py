from smartcard.System import readers
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.Exceptions import CardConnectionException
import ndef
import json
import threading
import time

class NDEFCardObserver(CardObserver):
    def __init__(self):
        self.card_processed = threading.Event()

    def update(self, _, cards):
        added_cards, removed_cards = cards

        for card in added_cards:
            print("📡 Card inserted")
            connection = card.createConnection()
            try:
                connection.connect()
            except CardConnectionException:
                print("❌ Failed to connect to card")
                return

            raw_data = []
            start_page = 4
            end_page = 39

            for page in range(start_page, end_page + 1, 4):
                READ_CMD = [0xFF, 0xB0, 0x00, page, 0x10]  # Read 16 bytes
                response, sw1, sw2 = connection.transmit(READ_CMD)
                if sw1 == 0x90 and sw2 == 0x00:
                    raw_data.extend(response)
                else:
                    print(f"❌ Failed to read page {page}: SW1={hex(sw1)} SW2={hex(sw2)}")
                    return

            try:
                ndef_start = raw_data.index(0x03)
                length = raw_data[ndef_start + 1]
                ndef_bytes = bytes(raw_data[ndef_start + 2 : ndef_start + 2 + length])
            except ValueError:
                print("❌ No NDEF TLV (0x03) found.")
                return
            except IndexError:
                print("❌ NDEF length exceeds available data.")
                return

            try:
                ndef_records = list(ndef.message_decoder(ndef_bytes))
                for record in ndef_records:
                    print(f"📦 Record Type: {record.type} (type: {type(record.type)})")
                    rtype = record.type
                    if isinstance(rtype, bytes):
                        rtype = rtype.decode('utf-8')
                    
                    if rtype == 'application/json':
                        json_payload = record.data.decode('utf-8')
                        try:
                            parsed = json.loads(json_payload)
                            print("✅ Decoded JSON:")
                            print(json.dumps(parsed, indent=2))
                        except json.JSONDecodeError:
                            print("⚠️ Invalid JSON, raw payload:")
                            print(json_payload)
                        self.card_processed.set()
                        return
                print("ℹ️ No application/json record found.")
            except Exception as e:
                print(f"❌ Failed to decode NDEF: {e}")


        for card in removed_cards:
            print("👋 Card removed")


def main():
    r = readers()
    if not r:
        print("❌ No smart card readers found.")
        return

    print("✅ Available readers:", r)
    print("📡 Waiting for card...")

    card_monitor = CardMonitor()
    observer = NDEFCardObserver()
    card_monitor.addObserver(observer)

    try:
        # Block until a card with valid data is processed
        observer.card_processed.wait()
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user.")
    finally:
        card_monitor.deleteObserver(observer)

if __name__ == "__main__":
    main()
