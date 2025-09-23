from redis import Redis

class SceneQueue:
    def __init__(self, redis_client: Redis, queue_name: str):
        self.redis = redis_client
        self.queue = queue_name

    def read_scene(self):
        try:
            result = self.redis.brpop(self.queue, timeout=5)
            if result is None:
                return None 
            _, value = result
            return value
        except Exception as e:
            print(f"Redis error: {e}", flush=True)
            return None

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

