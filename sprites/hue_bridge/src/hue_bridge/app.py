class App:
    def __init__(self, queue, subscriber):
        self.queue = queue

        self.subscriber = subscriber

    def run(self):
        try:
            while True:
                message = self.queue.get()
                print(message)
        except KeyboardInterrupt:
            print("Shutting down...")
            self.subscriber.close()
