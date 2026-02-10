# Version: 2026.02.10

class ModuleInterface:
    def __init__(self, config = None):
        pass

    @staticmethod
    def get_info():
        return {
            "name": __name__,  # interne id
            "display_name": __name__,
            "icon": "bi-cog",
            "type": "module"  # oder "submodule"
        }

    def install(self, confirm: bool = False) -> bool:
        raise NotImplementedError()

    def uninstall(self, confirm: bool = False) -> bool:
        raise NotImplementedError()