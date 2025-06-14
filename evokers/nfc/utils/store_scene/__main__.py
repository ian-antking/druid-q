from smartcard.System import readers
from smartcard.Exceptions import CardConnectionException, NoCardException
import time
import json

def wait_for_card(reader):
    print("📡 Waiting for card... Please place your card on the reader.")
    while True:
        try:
            connection = reader.createConnection()
            connection.connect()
            print("✅ Card detected!")
            return connection
        except (CardConnectionException, NoCardException):
            time.sleep(0.5)

def get_reader():
    r = readers()
    if len(r) == 0:
        raise Exception("No smart card readers found")
    print("✅ Available readers:", r)
    return r[0]

def get_uid(connection):
    GET_UID_CMD = [0xFF, 0xCA, 0x00, 0x00, 0x00]
    response, sw1, sw2 = connection.transmit(GET_UID_CMD)
    if sw1 == 0x90 and sw2 == 0x00:
        uid_hex = ''.join(f"{b:02x}" for b in response)
        return uid_hex
    else:
        raise Exception(f"Failed to get UID: SW1={hex(sw1)}, SW2={hex(sw2)}")

def main():
    reader = get_reader()
    connection = wait_for_card(reader)

    uid = get_uid(connection)
    print(f"UID read from card: {uid}")

    scene_name = input("Enter scene name: ").strip()
    description = input("Enter description (optional): ").strip()

    payload_dict = {
        "topic": "game/scene",
        "message": {
            "scene": scene_name,
            "description": description if description else None
        }
    }

    # Remove description if empty to keep it clean
    if not payload_dict["message"]["description"]:
        del payload_dict["message"]["description"]

    entry = {
        uid: payload_dict
    }

    print("\nAdd this entry to your card_data.json mapping file:\n")
    print(json.dumps(entry, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
