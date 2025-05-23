from app.lib.Backend import Backend
from app.modules.gmrender_resurrect.GmrenderResurrectModule import GmrenderResurrectModule
from app.modules.shairport_sync.ShairportSyncModule import ShairportSyncModule
from app.modules.system.SystemModule import SystemModule
from app.modules.usb.USBModule import USBModule


def register_modules():
    b = Backend()
    # TODO: Add config to modules

    b.add_module('usb', USBModule)
    b.add_module('system', SystemModule)
    b.add_module('shairport_sync', ShairportSyncModule)
    b.add_module('gmrender_resurrect', GmrenderResurrectModule)
