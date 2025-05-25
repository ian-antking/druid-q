import threading
import time
from queue import Queue, Empty
from rich.console import Console
from rich.panel import Panel
from event import Event, InfoEvent

from strings import MESSAGES

class ScreenManager:
    def __init__(self):
        self._event_queue = Queue()
        self._console = Console()
        self._running = True
        self._latest_info = "🔄 Waiting for events..."

        self._thread = threading.Thread(target=self.run, daemon=True)
        self._thread.start()

    def run(self):
        self._console.clear()

        while self._running:
            try:
                info = self._event_queue.get(timeout=0.1)
                self._latest_info = info
            except Empty:
                pass

            self._console.clear()
            self._console.print(
                Panel(self._latest_info, title=MESSAGES["latest_events"], expand=False)
            )
            time.sleep(0.5) 

    def update(self, event: Event):
        if isinstance(event, InfoEvent):
            self._event_queue.put(event.payload)

    def stop(self):
        self._running = False
        self._thread.join()
