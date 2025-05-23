

class ModuleInterface:
    @staticmethod
    def get_info():
        return {
            "name": __name__,  # interne id
            "display_name": __name__,
            "icon": "bi-cog",
            "type": "module"  # oder "submodule"
        }