from app.lib.Backend import Backend
from app.modules.bluetooth.BluetoothModule import BluetoothModule
from app.modules.ethernet.EthernetModule import EthernetModule
from app.modules.gmrender_resurrect.GmrenderResurrectModule import GmrenderResurrectModule
from app.modules.shairport_sync.ShairportSyncModule import ShairportSyncModule
from app.modules.system.SystemModule import SystemModule
from app.modules.usb.USBModule import USBModule
from app.modules.wifi.WifiModule import WifiModule


def register_modules():
    b = Backend()
    # TODO: Add config to modules

    b.add_module('wifi', WifiModule)
    b.add_module('ethernet', EthernetModule)
    b.add_module('bluetooth', BluetoothModule)
    # Network
    # b.add_module('usb', NetworkModule)
    b.add_module('usb', USBModule)
    b.add_module('system', SystemModule)
    # Audio

    # Submodules
    b.add_module('shairport_sync', ShairportSyncModule)
    b.add_module('gmrender_resurrect', GmrenderResurrectModule)