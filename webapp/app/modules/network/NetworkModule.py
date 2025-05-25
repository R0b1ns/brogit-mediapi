from app.lib.ModuleInterface import ModuleInterface
from app.modules.network.NetworkInterfaceManager import NetworkInterfaceManager


class NetworkModule(ModuleInterface):
    def __init__(self, config):
        super().__init__(config)
        self.config = config

    @staticmethod
    def get_info():
        return {
            "name": "network",  # interne id
            "display_name": "Network",
            "icon": "bi-hdd-network",
            "type": "module",  # oder "submodule"
            'has_settings': True
        }

    def interface(self, name: str = "ethernet") -> NetworkInterfaceManager:
        # TODO: Get interfaces and validate and choose ethernet and wlan adapter
        choose_adapter = {
            'ethernet': 'eth0',
            'wlan': 'wlan0'
        }

        i = NetworkInterfaceManager(self.config)
        i.default_interface = choose_adapter[name]
        return i