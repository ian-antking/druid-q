import queue
from events import InfoEvent, GameEvent
from .strings import MESSAGES

class App:
    def __init__(self, screen, event_queue, observer, publisher):
        self.screen = screen
        self.event_queue = event_queue
        self.observer = observer
        self.publisher = publisher

    def run(self):
        from smartcard.System import readers
        readers_list = readers()
        if not readers_list:
            self.screen.update(InfoEvent(MESSAGES["no_reader"]))
            return
        self.screen.update(InfoEvent(MESSAGES["available_readers"].format(readers=readers_list)))

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
            if hasattr(self.observer, "stop"):
                self.observer.stop()
            self.publisher.close()
            self.screen.stop()
