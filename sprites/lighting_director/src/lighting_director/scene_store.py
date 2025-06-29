import json

class SceneStore:
    def __init__(self, redis_client):
        self.redis = redis_client

    def get_cached_scene(self, scene_id: str):
        try:
            return self.redis.get(f"lighting_scene:{scene_id}")
        except Exception as e:
            print(f"Redis error in get_cached_scene: {e}", flush=True)
            return None

    def cache_scene(self, scene_id: str, scene_data: str):
        try:
            self.redis.set(f"lighting_scene:{scene_id}", scene_data)
        except Exception as e:
            print(f"Redis error in cache_scene: {e}", flush=True)

    def enqueue_scene(self, scene_data: str):
        try:
            self.redis.rpush("lighting_controller", scene_data)
        except Exception as e:
            print(f"Redis error in enqueue_scene: {e}", flush=True)

    def save_latest_scene(self, scene):
        try:
            self.redis.set("latest_scene", json.dumps(scene), ex=86400)
        except Exception as e:
            print(f"Redis error in save_latest_scene: {e}", flush=True)

    def get_latest_scene(self):
        try:
            data = self.redis.get("latest_scene")
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Redis error in get_latest_scene: {e}", flush=True)
            return None
