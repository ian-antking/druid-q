import board
import busio
import threading
import json
import time
import ndef
from adafruit_pn532.i2c import PN532_I2C

from events import InfoEvent, GameEvent
from .observer import Observer
from nfc.strings import MESSAGES


class PN532(Observer):
    def __init__(self, event_queue=None, poll_interval=0.5):
        super().__init__(event_queue)
        self.card_processed = threading.Event()
        self.poll_interval = poll_interval
        self.running = True
        self._last_uid = None

        # I2C setup for Raspberry Pi
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pn532 = PN532_I2C(i2c, debug=False)
        self.pn532.SAM_configuration()

        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def emit(self, event):
        self.event_queue.put(event)

    def _poll_loop(self):
        while self.running:
            uid = self.pn532.read_passive_target(timeout=0.5)

            added = []
            removed = []

            if uid:
                if uid != self._last_uid:
                    added.append(uid)
            elif self._last_uid:
                removed.append(self._last_uid)

            if added or removed:
                self.update(None, (added, removed))

            self._last_uid = uid
            time.sleep(self.poll_interval)

    def update(self, _, cards):
        added_cards, removed_cards = cards

        for uid in added_cards:
            self.emit(InfoEvent(MESSAGES["card_inserted"]))

            raw_data = bytearray()
            for page in range(4, 40):
                try:
                    data = self.pn532.ntag2xx_read_block(page)
                    if data:
                        raw_data.extend(data)
                    else:
                        self.emit(InfoEvent(MESSAGES["failed_read_page"].format(page=page, sw1="N/A", sw2="N/A")))
                        return
                except Exception as e:
                    self.emit(InfoEvent(MESSAGES["failed_read_page"].format(page=page, sw1="EXC", sw2=str(e))))
                    return

            try:
                ndef_start = raw_data.index(0x03)
                length = raw_data[ndef_start + 1]
                ndef_bytes = bytes(raw_data[ndef_start + 2 : ndef_start + 2 + length])
            except ValueError:
                self.emit(InfoEvent(MESSAGES["no_ndef"]))
                return
            except IndexError:
                self.emit(InfoEvent(MESSAGES["ndef_too_long"]))
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
                            self.emit(InfoEvent(MESSAGES["decoded_json"]))
                            self.emit(GameEvent(parsed["topic"], parsed["message"]))
                        except json.JSONDecodeError:
                            self.emit(InfoEvent(MESSAGES["invalid_json"].format(payload=json_payload)))
                        self.card_processed.set()
                        return
                self.emit(InfoEvent(MESSAGES["no_json_record"]))
            except Exception as e:
                self.emit(InfoEvent(MESSAGES["failed_decode"].format(error=e)))

        for _ in removed_cards:
            self.emit(InfoEvent(MESSAGES["card_removed"]))

    def stop(self):
        self.running = False
        self._thread.join()
