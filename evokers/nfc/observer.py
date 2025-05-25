import threading
import json
import queue
from smartcard.Exceptions import CardConnectionException
from smartcard.CardMonitoring import CardObserver
import ndef

class NFCCardObserver(CardObserver):
    def __init__(self, data_queue=None):
        self.card_processed = threading.Event()
        self.data_queue = data_queue or queue.Queue()

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
                        self.data_queue.put(parsed)
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