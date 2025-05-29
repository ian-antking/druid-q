from abc import ABC, abstractmethod
from events import Event

class Screen(ABC):
    @abstractmethod
    def update(self, event: Event):
        pass

    @abstractmethod
    def stop(self):
        pass
