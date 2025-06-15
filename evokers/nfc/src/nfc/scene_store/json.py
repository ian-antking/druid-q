import json
from typing import Optional
from .scene_store import SceneStore

class JsonSceneStore(SceneStore):
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._scenes = self._load_scenes()

    def _load_scenes(self) -> dict:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[SceneStore] Failed to load scenes from {self.filepath}: {e}")
            return {}

    def get_scene(self, scene_id: str) -> Optional[dict]:
        return self._scenes.get(scene_id)
