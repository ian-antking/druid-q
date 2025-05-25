import threading

class ScreenManager:
    def __init__(self):
        self._thread = threading.Thread(target=self.run, daemon=True)
        self._thread.start()

    def run(self):
        """Start the TUI loop or display logic."""
        print("🖥️ ScreenManager run loop started")
        # Replace with your actual TUI logic, e.g. loop with curses/textual

    def update(self, payload):
        """Update the display based on a new event payload."""
        print(f"🆕 ScreenManager received update: {payload}")
        # Apply update to TUI state
