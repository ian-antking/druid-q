from lighting_controller.scene_queue import SceneQueue
from lighting_controller.hue import Hue

class App:
    def __init__(self, queue: SceneQueue, hue: Hue):
        self.queue = queue
        self.hue = hue

    def run(self):
        while True:
            message = self.queue.read_scene()
            if message:
                self.hue.set_lights(message)
