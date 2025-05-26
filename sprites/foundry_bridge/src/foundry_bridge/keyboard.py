import pyautogui
from events import SceneChangeEvent

class KeyboardManager:
    def __init__(self, scene_to_key_map: dict[str, str]):
        """
        scene_to_key_map: Dict mapping scene names to keystrokes/macros.
        Example: { "Tavern": "ctrl+1", "Dungeon": "ctrl+2" }
        """
        self.scene_to_key_map = scene_to_key_map

    def handle_scene_change(self, event: SceneChangeEvent):
        scene_name = event.scene
        if not scene_name:
            print("⚠️ No scene name in event payload.")
            return

        key_combo = self.scene_to_key_map.get(scene_name)
        if not key_combo:
            print(f"⚠️ No keybinding configured for scene '{scene_name}'")
            return

        print(f"🎬 Changing to scene '{scene_name}' -> Triggering '{key_combo}'")
        pyautogui.hotkey(*key_combo.split('+'))
