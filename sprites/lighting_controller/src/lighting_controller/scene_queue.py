from redis import Redis

class SceneQueue:
    def __init__(self, redis_client: Redis, queue_name: str):
        self.redis = redis_client
        self.queue = queue_name

    def read_scene(self):
        try:
            return self.redis.rpop(self.queue)
        except Exception as e:
            print(f"Redis error: {e}", flush=True)

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

