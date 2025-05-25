from smartcard.System import readers
from smartcard.Exceptions import CardConnectionException, NoCardException
import ndef
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
            time.sleep(0.5)  # retry every half second


def get_reader():
    r = readers()
    if len(r) == 0:
        raise Exception("No smart card readers found")
    print("✅ Available readers:", r)
    return r[0]

def write_ndef(connection, ndef_message):
    # Prepare TLV: 0x03 + length + message + 0xFE terminator
    data = list(ndef_message)
    tlv = [0x03, len(data)] + data + [0xFE]
    while len(tlv) % 4 != 0:
        tlv.append(0x00)  # pad to multiple of 4 bytes

    for i in range(0, len(tlv), 4):
        page = tlv[i:i+4]
        page_number = 4 + i // 4
        WRITE_CMD = [0xFF, 0xD6, 0x00, page_number, 0x04] + page
        response, sw1, sw2 = connection.transmit(WRITE_CMD)
        if sw1 != 0x90 or sw2 != 0x00:
            print(f"❌ Failed to write page {page_number}: SW1={hex(sw1)} SW2={hex(sw2)}")
            return False
    print("✅ Write successful!")
    return True

if __name__ == "__main__":
    reader = get_reader()

    scene_name = input("Enter scene name: ").strip()
    print(f"Scene name entered: '{scene_name}'")

    print("Now, please place your NFC card on the reader to write the data.")
    connection = wait_for_card(reader)

    payload_dict = {
        "topic": "game/scene",
        "message": {
            "scene": scene_name
        }
    }
    json_payload = json.dumps(payload_dict, ensure_ascii=False)
    ndef_record = ndef.Record('application/json', data=json_payload.encode('utf-8'))
    ndef_message = b''.join(ndef.message_encoder([ndef_record]))

    success = write_ndef(connection, ndef_message)
    if success:
        print("Done writing to the card!")
    else:
        print("Writing failed.")
