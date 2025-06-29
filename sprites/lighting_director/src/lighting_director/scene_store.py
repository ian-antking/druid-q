import json

class SceneStore:
    def __init__(self, redis_client):
        self.redis = redis_client

    def save_latest_scene(self, scene):
        try:
            self.redis.set("latest_scene", json.dumps(scene))
        except Exception as e:
            print(f"Redis error: {e}", flush=True)

    def get_latest_scene(self):
        try:
            data = self.redis.get("latest_scene")
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Redis error: {e}", flush=True)
            return None
