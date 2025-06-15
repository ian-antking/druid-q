import threading
from .observer import Observer
from smartcard.Exceptions import CardConnectionException
from smartcard.CardMonitoring import CardMonitor
from smartcard.System import readers

from events import InfoEvent, CardReadEvent
from nfc.strings import MESSAGES

class ACR122U(Observer):
    def __init__(self, event_queue=None):
        super().__init__(event_queue)
        self.card_processed = threading.Event()
        self.monitor = CardMonitor()
        self.readers = readers()

        if self.readers is None or len(self.readers) == 0:
            self.emit(InfoEvent(MESSAGES["no_reader"]))
            raise RuntimeError("No smartcard readers found for ACR122U")

        self.monitor.addObserver(self)

    def stop(self):
        self.monitor.deleteObserver(self)

    def emit(self, event):
        self.event_queue.put(event)

    def update(self, _, cards):
        added_cards, removed_cards = cards

        for card in added_cards:
            self.emit(InfoEvent(MESSAGES["card_inserted"]))
            connection = card.createConnection()
            try:
                connection.connect()
            except CardConnectionException:
                self.emit(InfoEvent(MESSAGES["failed_connect"]))
                return

            try:
                uid = self._read_uid(connection)
                if uid:
                    self.emit(InfoEvent(f"📡 Card inserted (UID: {uid})"))
                    self.emit(CardReadEvent(uid))
            except Exception as e:
                self.emit(InfoEvent(f"❌ Failed to read UID: {e}"))

        for card in removed_cards:
            self.emit(InfoEvent(MESSAGES["card_removed"]))

    def _read_uid(self, connection):
        GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
        response, sw1, sw2 = connection.transmit(GET_UID)
        if sw1 == 0x90 and sw2 == 0x00:
            return ''.join(f'{b:02x}' for b in response)
        raise ValueError(f"Failed to get UID (SW1: {hex(sw1)}, SW2: {hex(sw2)})")
