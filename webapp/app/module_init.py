from flask import Blueprint

from app.lib.Backend import Backend
from app.modules.audio.AudioModule import AudioModule
from app.modules.bluetooth.BluetoothModule import BluetoothModule
from app.modules.ethernet.EthernetModule import EthernetModule
from app.modules.gmrender_resurrect.GmrenderResurrectModule import GmrenderResurrectModule
from app.modules.network.NetworkModule import NetworkModule
from app.modules.shairport_sync.ShairportSyncModule import ShairportSyncModule
from app.modules.system.SystemModule import SystemModule
from app.modules.usb.USBModule import USBModule
from app.modules.wifi.WifiModule import WifiModule


def register_modules(app, config):
    # TODO: Combine that in one generic solution
    m = Modules()

    m.add_module('wifi')
    m.add_module('ethernet')
    m.add_module('bluetooth')

    m.add_module('network')
    m.add_module('usb')
    m.add_module('system')

    app.register_blueprint(m.get_blueprint())

    b = Backend(config)

    b.add_module('wifi', WifiModule)
    b.add_module('ethernet', EthernetModule)
    b.add_module('bluetooth', BluetoothModule)
    b.add_module('network', NetworkModule)
    b.add_module('usb', USBModule)
    b.add_module('system', SystemModule)
    b.add_module('audio', AudioModule)

    # Submodules
    b.add_module('shairport_sync', ShairportSyncModule)
    b.add_module('gmrender_resurrect', GmrenderResurrectModule)

import importlib

class Modules:
    def __init__(self, module_path='app.modules'):
        self.module_path = module_path
        self.loaded_modules = {}

        self.module_bp = Blueprint('module', __name__, url_prefix='/module')

    def get_blueprint(self):
        return self.module_bp

    def add_module(self, name):
        full_path = f"{self.module_path}.{name}"
        mod = importlib.import_module(full_path)

        # Suche nach einem Attribut wie "network_bp"
        for attr in dir(mod):
            obj = getattr(mod, attr)
            if hasattr(obj, 'name') and hasattr(obj, 'route'):
                # Sieht aus wie ein Blueprint
                self.module_bp.register_blueprint(obj)
                self.loaded_modules[name] = obj
                break
        else:
            raise ValueError(f"No blueprint found in module {name}")
