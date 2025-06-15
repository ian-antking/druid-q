from abc import ABC, abstractmethod
from typing import Optional

class SceneStore(ABC):
    """Abstract base class for a scene store."""

    @abstractmethod
    def get_scene(self, scene_id: str) -> Optional[dict]:
        """
        Retrieve the scene data associated with the given scene ID (e.g. card UID).
        
        Returns:
            dict if scene is found, else None.
        """
        pass
