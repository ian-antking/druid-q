from abc import ABC, abstractmethod

class Observer(ABC):
    def __init__(self, event_queue=None):
        self.event_queue = event_queue

    def emit(self, event):
        if self.event_queue:
            self.event_queue.put(event)

    @abstractmethod
    def update(self, subject, cards):
        """Called when observed cards change: (added_cards, removed_cards)"""
        pass

    def stop(self):
        """Optional cleanup method; subclasses may override if needed."""
        pass
