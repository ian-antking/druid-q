from abc import ABC, abstractmethod
from events import SceneChangeEvent

class EventValidator(ABC):
    @abstractmethod
    def run(self, message: dict) -> bool:
        """Validate the incoming message dict."""
        pass

class SceneChangeEventValidator(EventValidator):
    def run(self, message: dict) -> bool:
        return isinstance(message, dict) and \
               'scene' in message and \
               isinstance(message['scene'], str)

    def parse(self, message: dict) -> SceneChangeEvent:
        if not self.run(message):
            raise ValueError("Invalid message")
        return SceneChangeEvent(scene=message['scene'])