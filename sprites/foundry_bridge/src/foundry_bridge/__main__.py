import queue
from dotenv import load_dotenv
import os
from .subscriber import Subscriber
from .strings import MESSAGES

def main():
    load_dotenv()

    DRUID_HOST = os.getenv("DRUID_HOST")
    DRUID_USERNAME = os.getenv("DRUID_USERNAME")
    DRUID_PASSWORD = os.getenv("DRUID_PASSWORD")
    DRUID_TOPIC = os.getenv("DRUID_TOPIC")

    if not (DRUID_HOST and DRUID_USERNAME and DRUID_PASSWORD):
        raise EnvironmentError(MESSAGES["missing_env_error"])

    q = queue.Queue()
    subscriber = Subscriber(DRUID_HOST, DRUID_USERNAME, DRUID_PASSWORD, DRUID_TOPIC, q)

    try:
        while True:
            message = q.get()
            print("Received message:", message)
    except KeyboardInterrupt:
        print("Shutting down...")
        subscriber.close()

if __name__ == "__main__":
    main()
