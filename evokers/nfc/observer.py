import threading
import json
import queue
from smartcard.Exceptions import CardConnectionException
from smartcard.CardMonitoring import CardObserver
import ndef
from event import Event
from strings import MESSAGES

class NFCCardObserver(CardObserver):

    def __init__(self, event_queue=None):
        self.card_processed = threading.Event()
        self.event_queue = event_queue or queue.Queue()

    def emit(self, type_, payload):
        self.event_queue.put(Event(type_, payload))

    def update(self, _, cards):
        added_cards, removed_cards = cards

        for card in added_cards:
            self.emit("info", MESSAGES["card_inserted"])
            connection = card.createConnection()
            try:
                connection.connect()
            except CardConnectionException:
                self.emit("info", MESSAGES["failed_connect"])
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
                    self.emit("info", MESSAGES["failed_read_page"].format(page=page, sw1=hex(sw1), sw2=hex(sw2)))
                    return

            try:
                ndef_start = raw_data.index(0x03)
                length = raw_data[ndef_start + 1]
                ndef_bytes = bytes(raw_data[ndef_start + 2 : ndef_start + 2 + length])
            except ValueError:
                self.emit("info", MESSAGES["no_ndef"])
                return
            except IndexError:
                self.emit("info", MESSAGES["ndef_too_long"])
                return

            try:
                ndef_records = list(ndef.message_decoder(ndef_bytes))
                for record in ndef_records:
                    rtype = record.type
                    if isinstance(rtype, bytes):
                        rtype = rtype.decode('utf-8')
                    
                    if rtype == 'application/json':
                        json_payload = record.data.decode('utf-8')
                        try:
                            parsed = json.loads(json_payload)
                            self.emit("info", MESSAGES["decoded_json"])
                            self.emit("game", parsed)
                        except json.JSONDecodeError:
                            self.emit("info", MESSAGES["invalid_json"].format(payload=json_payload))
                        self.card_processed.set()
                        return
                self.emit("info", MESSAGES["no_json_record"])
            except Exception as e:
                self.emit("info", MESSAGES["failed_decode"].format(error=e))

        for card in removed_cards:
            self.emit("info", MESSAGES["card_removed"])
