import queue
from smartcard.System import readers
from smartcard.CardMonitoring import CardMonitor
from events import InfoEvent, GameEvent
from .strings import MESSAGES

class App:
    def __init__(
        self,
        screen,
        event_queue: queue.Queue,
        observer,
        publisher,
        monitor: CardMonitor = None,
    ):
        self.screen = screen
        self.event_queue = event_queue
        self.observer = observer
        self.publisher = publisher
        self.card_monitor = monitor

    def run(self):
        readers_list = readers()
        if not readers_list and self.card_monitor is not None:
            self.screen.update(InfoEvent(MESSAGES["no_reader"]))
            return

        if self.card_monitor is not None:
            self.screen.update(InfoEvent(MESSAGES["available_readers"].format(readers=readers_list)))
            self.card_monitor.addObserver(self.observer)

        # Start the observer if it has a start method (e.g., PN532Observer)
        if hasattr(self.observer, "start") and callable(self.observer.start):
            self.observer.start()

        try:
            while True:
                try:
                    event = self.event_queue.get(timeout=1)
                    if isinstance(event, GameEvent):
                        self.publisher.publish(event.payload)
                        self.screen.update(InfoEvent(MESSAGES["published_event"].format(event=event.payload)))
                    else:
                        self.screen.update(event)
                except queue.Empty:
                    continue
        except KeyboardInterrupt:
            self.screen.update(InfoEvent(MESSAGES["user_interrupt"]))
        finally:
            # Stop the observer if it has a stop method
            if hasattr(self.observer, "stop") and callable(self.observer.stop):
                self.observer.stop()

            if self.card_monitor is not None:
                self.card_monitor.deleteObserver(self.observer)

            self.publisher.close()
            self.screen.stop()
