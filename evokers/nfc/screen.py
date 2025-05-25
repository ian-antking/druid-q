import threading
import time
from queue import Queue, Empty
from rich.console import Console
from rich.panel import Panel
from event import Event, InfoEvent

class ScreenManager:
    def __init__(self):
        self._event_queue = Queue()
        self._console = Console()
        self._running = True
        self._latest_info = "🔄 Waiting for events..."

        self._thread = threading.Thread(target=self.run, daemon=True)
        self._thread.start()

    def run(self):
        """Start the screen manager display loop."""
        self._console.clear()
        self._console.print("🖥️ [bold green]ScreenManager started[/bold green]")

        while self._running:
            try:
                # Poll the event queue for new info updates
                info = self._event_queue.get(timeout=0.1)
                self._latest_info = info
            except Empty:
                pass

            # Redraw the screen with the latest info
            self._console.clear()
            self._console.print(
                Panel(self._latest_info, title="📡 Latest Info Event", expand=False)
            )
            time.sleep(0.5)  # Simple render throttle

    def update(self, event: Event):
        """Send a new info event to the display loop."""

        if isinstance(event, InfoEvent):
            self._event_queue.put(event.payload)

    def stop(self):
        """Optional stop method if you ever want to shut down gracefully."""
        self._running = False
        self._thread.join()
