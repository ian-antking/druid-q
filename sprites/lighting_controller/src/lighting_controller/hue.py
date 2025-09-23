import requests

def discover_bridge_ip():
    response = requests.get("https://discovery.meethue.com/")
    response.raise_for_status()
    bridges = response.json()
    if not bridges:
        raise RuntimeError("No bridges found")
    return bridges[0]["internalipaddress"]

class Hue:
    def __init__(self, bridge_ip: str):
        self.bridge_ip = bridge_ip

    def set_lights(self, light_setting):
        print(light_setting)
