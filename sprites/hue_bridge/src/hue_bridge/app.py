import json

class App:
    def __init__(self, queue, subscriber, redis_client):
        self.queue = queue
        self.subscriber = subscriber
        self.redis = redis_client

    def run(self):
        try:
            while True:
                message = self.queue.get()
                print(message, flush=True)
                try:
                    self.redis.rpush("last_event", json.dumps(message))
                except Exception as e:
                    print(f"Redis error: {e}", flush=True)
        except KeyboardInterrupt:
            print("Shutting down...", flush=True)
            self.subscriber.close()
