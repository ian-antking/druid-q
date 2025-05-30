class App:
    def __init__(self, queue, subscriber, keyboardManager):
        self.queue = queue

        self.subscriber = subscriber
        self.keyboard = keyboardManager

    def run(self):
        try:
            while True:
                message = self.queue.get()
                self.keyboard.handle_scene_change(message)
        except KeyboardInterrupt:
            print("Shutting down...")
            self.subscriber.close()