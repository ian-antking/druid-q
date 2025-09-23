import os
from dotenv import load_dotenv
from .app import App

load_dotenv()

HUE_API_KEY = os.getenv("HUE_API_KEY")
ROOM_NAME = os.getenv("ROOM_NAME")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

def main() :
    print(HUE_API_KEY)
    print(ROOM_NAME)
    print(REDIS_HOST)

    app = App()

    app.run()

if __name__ == "__main__":
    main()
