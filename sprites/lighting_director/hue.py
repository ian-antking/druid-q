import requests

def discover_bridge_ip():
    response = requests.get("https://discovery.meethue.com/")
    response.raise_for_status()
    bridges = response.json()
    if not bridges:
        raise RuntimeError("No bridges found")
    return bridges[0]["internalipaddress"]

def get_lights_in_room(room_name: str, api_key: str, bridge_ip: str):
    headers = {
        "hue-application-key": api_key
    }

    url = f"https://{bridge_ip}/clip/v2/resource/room"
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()

    rooms = response.json().get("data", [])

    target_room = next((room for room in rooms if room["metadata"]["name"].lower() == room_name.lower()), None)
    if not target_room:
        raise ValueError(f"Room '{room_name}' not found")

    lights = []
    for light in target_room.get("children", []):
        light_id = light["rid"]
        light_url = f"https://{bridge_ip}/clip/v2/resource/device/{light_id}"
        light_resp = requests.get(light_url, headers=headers, verify=False)
        light_resp.raise_for_status()
        lights.append(light_resp.json().get("data", [{}])[0])

    return clean_hue_light_metadata(lights)

def clean_hue_light_metadata(devices):
    return {
        "lights": [
            {
                "id": d["id"],
                "name": d["metadata"]["name"],
                "type": d["product_data"]["product_name"],
                "archetype": d["metadata"].get("archetype", d["product_data"].get("product_archetype", "unknown")),
            }
            for d in devices
        ]
    }
