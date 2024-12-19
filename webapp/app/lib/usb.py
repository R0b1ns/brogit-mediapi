import usb.core


def list_usb_devices():
    devices = usb.core.find(find_all=True)
    usb_devices = []
    for device in devices:
        usb_devices.append({
            "idVendor": hex(device.idVendor),
            "idProduct": hex(device.idProduct),
            "serial_number": device.serial_number,
        })
    return usb_devices
