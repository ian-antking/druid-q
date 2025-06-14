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
        try:
            while True:
                try:
                    event = self.event_queue.get(timeout=1)
                    print(f"Got event from queue: {event}")
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
