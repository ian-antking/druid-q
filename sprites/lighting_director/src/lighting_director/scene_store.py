import json

class SceneStore:
    def __init__(self, redis_client):
        self.redis = redis_client

    def get_room_lights(self):
        try:
            return self.redis.get(f"room_lights")
        except Exception as e:
            print(f"Redis error in get_room_lights: {e}", flush=True)
            return None
        
    def set_room_lights(self, light_data):
        try:
            self.redis.set("room_lights", light_data)
        except Exception as e:
            print(f"Redis error in set_hue_ip: {e}", flush=True)

    def get_hue_ip(self):
        try:
            return self.redis.get(f"hue_ip")
        except Exception as e:
            print(f"Redis error in get_hue_ip: {e}", flush=True)
            return None

    def set_hue_ip(self, hue_ip):
        try:
            self.redis.set("hue_ip", hue_ip)
        except Exception as e:
            print(f"Redis error in set_hue_ip: {e}", flush=True)


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
