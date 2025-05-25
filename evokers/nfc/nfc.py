from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.Exceptions import NoCardException
import time

def get_reader():
    r = readers()
    if len(r) == 0:
        raise Exception("No smart card readers found")
    print("Available readers:", r)
    return r[0]

def read_uid():
    reader = get_reader()
    connection = reader.createConnection()

    try:
        connection.connect()
    except NoCardException:
        # No card is inserted right now
        return None

    # APDU command to get UID from MIFARE classic / NFC tag (standard command)
    GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]

    response, sw1, sw2 = connection.transmit(GET_UID)

    if sw1 == 0x90 and sw2 == 0x00:
        uid = toHexString(response).replace(" ", "")
        print("UID:", uid)
        return uid
    else:
        print(f"Failed to get UID, SW1={hex(sw1)} SW2={hex(sw2)}")
        return None

if __name__ == "__main__":
    while True:
        uid = read_uid()
        if uid:
            print("Tag UID:", uid)
        else:
            print("No tag detected, please place a card on the reader.")
        time.sleep(1)
