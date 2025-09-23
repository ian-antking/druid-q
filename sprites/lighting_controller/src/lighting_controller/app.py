from lighting_controller.scene_queue import SceneQueue

class App:
    def __init__(self, queue: SceneQueue):
        self.queue = queue

    def run(self):
        while True:
            message = self.queue.read_scene()
            print(message)
