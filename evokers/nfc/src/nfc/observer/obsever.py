from abc import ABC, abstractmethod
from events import Event
import queue

class Observer(ABC):
    def __init__(self, event_queue: queue.Queue):
        self.event_queue = event_queue

    @abstractmethod
    def start(self):
        """Start any internal threads or monitoring required"""
        pass

    @abstractmethod
    def stop(self):
        """Clean up threads or monitoring when app is shutting down"""
        pass