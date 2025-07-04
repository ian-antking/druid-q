from dataclasses import asdict
import base64
import json
from queue import Queue

from lighting_director.llm import LLMClient
from lighting_director.scene_store import SceneStore
from subscriber import Subscriber

class App:
    def __init__(self, queue: Queue, subscriber: Subscriber, scene_store: SceneStore, llm_client: LLMClient):
        self.queue = queue
        self.subscriber = subscriber
        self.scene_store = scene_store
        self.llm_client = llm_client

    def run(self):
        try:
            while True:
                message = self.queue.get()
                print(message, flush=True)
                parsed_message = asdict(message)
                try:
                    json_bytes = json.dumps(parsed_message).encode("utf-8")
                    b64_scene = base64.b64encode(json_bytes).decode("utf-8")

                    current_scene = self.scene_store.get_latest_scene()

                    if current_scene == b64_scene:
                        print("Scene unchanged, skipping Redis write.", flush=True)
                        continue 

                    self.scene_store.save_latest_scene(b64_scene)
                    print("Scene updated in Redis.", flush=True)

                    scene_data = self.scene_store.get_cached_scene(b64_scene)

                    if scene_data == None :
                        scene_data = json.dumps(self.llm_client.generate_scene_design(parsed_message["scene"], parsed_message["description"]))
                        self.scene_store.cache_scene(scene_id=b64_scene, scene_data=scene_data)

                    self.scene_store.enqueue_scene(scene_data)

                except Exception as e:
                    print(f"Error storing scene: {e}", flush=True)
        except KeyboardInterrupt:
            print("Shutting down...", flush=True)
            self.subscriber.close()
