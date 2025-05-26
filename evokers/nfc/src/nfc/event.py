from dataclasses import dataclass
from typing import Literal, Union, Dict

@dataclass
class Event:
    type: Literal["info", "game"]

@dataclass
class InfoEvent(Event):
    payload: str

    def __init__(self, message: str):
        super().__init__(type="info")
        self.payload = message

@dataclass
class GameEvent(Event):
    payload: Dict[str, str]

    def __init__(self, topic: str, message: str):
        super().__init__(type="game")
        self.payload = {"topic": topic, "message": message}