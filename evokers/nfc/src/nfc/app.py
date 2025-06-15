import queue
from events import InfoEvent, GameEvent, CardReadEvent
from .strings import MESSAGES

class App:
    def __init__(self, screen, event_queue, observer, publisher, scene_store):
        self.screen = screen
        self.event_queue = event_queue
        self.observer = observer
        self.publisher = publisher
        self.scene_store = scene_store

    def run(self):
        try:
            while True:
                try:
                    event = self.event_queue.get(timeout=1)
                    print(f"Got event from queue: {event}")

                    if isinstance(event, CardReadEvent):
                        scene = self.scene_store.get_scene(event.uid)
                        if scene:
                            topic = scene.get("topic")
                            message = scene.get("message")
                            if topic and message:
                                game_event = GameEvent(topic, message)
                                self.publisher.publish(game_event.payload)
                                self.screen.update(InfoEvent(MESSAGES["published_event"].format(event=game_event.payload)))
                            else:
                                self.screen.update(InfoEvent("❌ Invalid scene format in store."))
                        else:
                            self.screen.update(InfoEvent("❌ Unknown card. No scene found."))

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
