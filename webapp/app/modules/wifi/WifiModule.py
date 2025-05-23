from app.lib.ModuleInterface import ModuleInterface


class WifiModule(ModuleInterface):
    @staticmethod
    def get_info():
        return {
            "name": "wifi",  # interne id
            "display_name": "Wifi",
            "icon": "bi-wifi",
            "type": "module"  # oder "submodule"
        }

    def is_connected(self) -> bool:
        if self.get_connection_info():
            return True
        else:
            return False

    def get_connection_info(self):
        pass