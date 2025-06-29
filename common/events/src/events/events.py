from dataclasses import dataclass, field
from typing import Literal, Dict

@dataclass
class Event:
    type: Literal["info", "game", "scene", "card"]

@dataclass
class InfoEvent(Event):
    type: Literal["info"] = field(default="info", init=False)
    payload: str

@dataclass
class GameEvent(Event):
    type: Literal["game"] = field(default="game", init=False)
    payload: Dict[str, str]

@dataclass
class SceneChangeEvent(Event):
    type: Literal["scene"] = field(default="scene", init=False)
    scene: str
    description: str

@dataclass
class CardReadEvent(Event):
    type: Literal["card"] = field(default="card", init=False)
    uid: str
