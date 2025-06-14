import board
import busio
import threading
import time
from adafruit_pn532.i2c import PN532_I2C

from events import InfoEvent, GameEvent
from .observer import Observer
from nfc.strings import MESSAGES
from .library import library

class PN532(Observer):
    def __init__(self, event_queue=None, poll_interval=0.5):
        super().__init__(event_queue)
        self.poll_interval = poll_interval
        self.running = True
        self._last_uid = None

        i2c = busio.I2C(board.SCL, board.SDA)
        self.pn532 = PN532_I2C(i2c, debug=False)

        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def emit(self, event):
        self.event_queue.put(event)

    def update(self, uid_hex):
        self.emit(InfoEvent(f"📡 Card inserted (UID: {uid_hex})"))

        entry = library.get(uid_hex)
        if not entry:
            self.emit(InfoEvent("❌ Unknown card. No scene found."))
            return

        topic = entry.get("topic")
        message = entry.get("message")

        if topic and message:
            self.emit(GameEvent(topic, message))
        else:
            self.emit(InfoEvent("❌ Invalid entry format."))

    def _poll_loop(self):
        while self.running:
            uid = self.pn532.read_passive_target(timeout=0.5)

            if uid:
                uid_hex = ''.join(f"{b:02x}" for b in uid)
                if uid_hex != self._last_uid:
                    self._last_uid = uid_hex
                    self.update(uid_hex)
            else:
                self._last_uid = None

            time.sleep(self.poll_interval)

    def stop(self):
        self.running = False
        self._thread.join()
