import bluetooth

def send_message(message):
    nearby_devices = bluetooth.discover_devices()

    for bdaddr in nearby_devices:
        print(bluetooth.lookup_name(bdaddr))
        if "Celine’s iPhone" == bluetooth.lookup_name( bdaddr ):
            target_address = bdaddr
            break

    if target_address is not None:
        port = 1
        sock = bluetooth.BluetoothSocket()
        sock.connect((target_address, port))
        sock.send(message.encode())
        sock.close()
        print("Message sent successfully.")
    else:
        print("Could not find target device.")

def get_nearby_devices():
    nearby_devices = bluetooth.discover_devices()

    for bdaddr in nearby_devices:
        print(bluetooth.lookup_name(bdaddr))


