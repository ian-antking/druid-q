import threading
import json
import queue
import time
from events import InfoEvent, GameEvent
from .strings import MESSAGES
from .observer import CardObserver  # keep the same base class for interface parity

# Import Waveshare PN532 library
from pn532 import PN532_SPI  # or PN532_I2C, PN532_UART depending on your connection

class PN532(CardObserver):
    def __init__(self, event_queue=None, spi_bus=0, spi_device=0, gpio_cs=22, gpio_reset=18):
        super().__init__()
        self.event_queue = event_queue or queue.Queue()
        self.card_processed = threading.Event()
        self._stop_event = threading.Event()

        # Initialize PN532 over SPI (adjust pins/bus/device as needed)
        self.pn532 = PN532_SPI(cs=gpio_cs, reset=gpio_reset, bus=spi_bus, device=spi_device)
        self.pn532.SAM_configuration()

        # Thread to poll cards
        self.thread = threading.Thread(target=self._poll_cards, daemon=True)

    def emit(self, event):
        self.event_queue.put(event)

    def start(self):
        self._stop_event.clear()
        self.thread.start()

    def stop(self):
        self._stop_event.set()
        self.thread.join()

    def _poll_cards(self):
        self.emit(InfoEvent(MESSAGES["waiting_for_card"]))
        while not self._stop_event.is_set():
            uid = self.pn532.read_passive_target(timeout=0.5)
            if uid is None:
                continue

            self.emit(InfoEvent(MESSAGES["card_inserted"]))
            try:
                # Read NDEF data from the card
                ndef_data = self._read_ndef()
                if not ndef_data:
                    self.emit(InfoEvent(MESSAGES["no_ndef"]))
                    continue

                # Decode NDEF message
                ndef_records = list(ndef.message_decoder(ndef_data))
                found_json = False

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
                            found_json = True
                            self.card_processed.set()
                            break
                        except json.JSONDecodeError:
                            self.emit(InfoEvent(MESSAGES["invalid_json"].format(payload=json_payload)))

                if not found_json:
                    self.emit(InfoEvent(MESSAGES["no_json_record"]))

            except Exception as e:
                self.emit(InfoEvent(MESSAGES["failed_decode"].format(error=e)))

            self.emit(InfoEvent(MESSAGES["card_removed"]))
            # Small delay to debounce multiple reads of same card
            time.sleep(1)

    def _read_ndef(self):
        """
        Read NDEF data from the PN532 card.
        This will depend on card type and how to read the memory.
        For simplicity, we’ll try to read pages 4-39 like ARC122U did.
        """

        raw_data = []

        try:
            # Read pages 4-39, 16 bytes each
            for page in range(4, 40, 4):
                # PN532 read command depends on card type, but PN532_SPI.read_mifare_block() can help
                # Read four blocks (4 bytes each) to make 16 bytes total
                for block in range(page, page + 4):
                    data = self.pn532.read_mifare_block(block)
                    if data is None:
                        self.emit(InfoEvent(MESSAGES["failed_read_page"].format(page=block, sw1="None", sw2="None")))
                        return None
                    raw_data.extend(data)

            # Locate NDEF TLV 0x03
            ndef_start = raw_data.index(0x03)
            length = raw_data[ndef_start + 1]
            ndef_bytes = bytes(raw_data[ndef_start + 2 : ndef_start + 2 + length])
            return ndef_bytes
        except ValueError:
            self.emit(InfoEvent(MESSAGES["no_ndef"]))
        except IndexError:
            self.emit(InfoEvent(MESSAGES["ndef_too_long"]))
        except Exception as e:
            self.emit(InfoEvent(MESSAGES["failed_read_page"].format(page="unknown", sw1=type(e).__name__, sw2=str(e))))

        return None
