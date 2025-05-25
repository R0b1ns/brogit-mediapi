from app.lib.ModuleInterface import ModuleInterface


class NetworkModule(ModuleInterface):
    @staticmethod
    def get_info():
        return {
            "name": "network",  # interne id
            "display_name": "Network",
            "icon": "bi-hdd-network",
            "type": "module",  # oder "submodule"
            'has_settings': True
        }
