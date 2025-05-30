class App:
    def __init__(self, queue, subscriber, keyboard_manager):
        self.queue = queue

        self.subscriber = subscriber
        self.keyboard = keyboard_manager

    def run(self):
        try:
            while True:
                message = self.queue.get()
                self.keyboard.handle_scene_change(message)
        except KeyboardInterrupt:
            print("Shutting down...")
            self.subscriber.close()