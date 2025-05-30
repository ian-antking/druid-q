import queue
import os
from smartcard.System import readers
from smartcard.CardMonitoring import CardMonitor
from events import InfoEvent, GameEvent
from .observer import CardObserver
from .publisher import Publisher
from .screen import Screen
from .strings import MESSAGES

class App:
    def __init__(
        self,
        screen: Screen,
        event_queue: queue.Queue,
        observer: CardObserver,
        publisher: Publisher,
        monitor: CardMonitor,
    ):
        self.screen = screen
        self.event_queue = event_queue
        self.observer = observer
        self.publisher = publisher
        self.card_monitor = monitor

    def run(self):
        readers_list = readers()
        if not readers_list:
            self.screen.update(InfoEvent(MESSAGES["no_reader"]))
            return

        self.screen.update(InfoEvent(MESSAGES["available_readers"].format(readers=readers_list)))
        self.card_monitor.addObserver(self.observer)

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
            self.card_monitor.deleteObserver(self.observer)
            self.publisher.close()
            self.screen.stop()
