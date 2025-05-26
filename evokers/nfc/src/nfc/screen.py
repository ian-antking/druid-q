import threading
import time
from queue import Queue, Empty
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.live import Live
from rich.theme import Theme
from rich import box
from events import Event, InfoEvent

from .strings import MESSAGES

custom_theme = Theme({
    "arcane": "bold magenta",
    "header": "bold cyan",
    "footer": "bold green",
    "info": "dim white",
})

class ScreenManager:
    def __init__(self):
        self._event_queue = Queue()
        self._console = Console(theme=custom_theme)
        self._running = True
        self._latest_info = MESSAGES["waiting_for_events"]

        self._thread = threading.Thread(target=self.run, daemon=True)
        self._thread.start()

    def _build_layout(self) -> Layout:
        layout = Layout()
        layout.split(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=3)
        )

        layout["header"].update(
            Panel(
                Text(MESSAGES["header_title"], style="header"),
                style="arcane",
                border_style="header",
                box=box.DOUBLE
            )
        )

        layout["footer"].update(
            Panel(
                Text(MESSAGES["footer_title"], style="footer"),
                border_style="footer",
                box=box.MINIMAL
            )
        )

        return layout

    def run(self):
        self._console.clear()
        layout = self._build_layout() 
        with Live(layout, console=self._console, refresh_per_second=5, screen=True) as live:
            while self._running:
                try:
                    info = self._event_queue.get(timeout=0.1)
                    self._latest_info = info
                except Empty:
                    pass

                body_panel = Panel(
                    Text(
                        self._latest_info,
                        style="info"
                    ),
                    title=MESSAGES["body_title"],
                    border_style="arcane",
                    box=box.ROUNDED,
                    style="on black"
                )
                layout["body"].update(body_panel)

                time.sleep(0.5) 

    def update(self, event: Event):
        if isinstance(event, InfoEvent):
            self._event_queue.put(event.payload)

    def stop(self):
        self._running = False
        self._thread.join()
