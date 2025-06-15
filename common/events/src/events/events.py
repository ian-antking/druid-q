from dataclasses import dataclass
from typing import Literal, Dict

@dataclass
class Event:
    type: Literal["info", "game", "scene"]

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

@dataclass
class SceneChangeEvent(Event):
    scene: str
    description: str  # <--- add this

    def __init__(self, scene: str, description: str):
        super().__init__(type="scene")
        self.scene = scene
        self.description = description

@dataclass
class CardReadEvent(Event):
    uid: str

    def __init__(self, uid: str):
        super().__init__(type="card")
        self.uid = uid