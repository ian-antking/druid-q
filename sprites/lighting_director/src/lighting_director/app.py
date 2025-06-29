from dataclasses import asdict
import base64
import json

class App:
    def __init__(self, queue, subscriber, scene_store):
        self.queue = queue
        self.subscriber = subscriber
        self.scene_store = scene_store

    def run(self):
        try:
            while True:
                message = self.queue.get()
                print(message, flush=True)
                try:
                    json_bytes = json.dumps(asdict(message)).encode("utf-8")
                    b64_scene = base64.b64encode(json_bytes).decode("utf-8")

                    current_scene = self.scene_store.get_latest_scene()

                    if current_scene == b64_scene:
                        print("Scene unchanged, skipping Redis write.", flush=True)
                        continue 

                    self.scene_store.store_scene(b64_scene)
                    print("Scene updated in Redis.", flush=True)

                except Exception as e:
                    print(f"Error storing scene: {e}", flush=True)
        except KeyboardInterrupt:
            print("Shutting down...", flush=True)
            self.subscriber.close()
