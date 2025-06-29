from python_hue_v2 import Hue
import asyncio
import requests

def discover_bridge_ip():
    response = requests.get("https://discovery.meethue.com/")
    response.raise_for_status()
    bridges = response.json()
    if not bridges:
        raise RuntimeError("No bridges found")
    return bridges[0]["internalipaddress"]

def get_lights_in_room(room_name: str, api_key: str, bridge_ip: str):
    async def get_lights():
        hue = Hue(bridge_ip, api_key)

        rooms = hue.rooms

        print(type(rooms[0]))
        print(dir(rooms[0]))

        lights = []

        return lights

    return asyncio.run(get_lights())
