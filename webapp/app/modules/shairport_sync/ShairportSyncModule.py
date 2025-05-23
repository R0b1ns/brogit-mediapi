from app.lib.ModuleInterface import ModuleInterface


class ShairportSyncModule(ModuleInterface):
    @staticmethod
    def get_info():
        return {
            "name": "shairport-sync",  # interne id
            "display_name": "ShairPort-Sync",
            "icon": "bi-cog",
            "type": "submodule"  # oder "submodule"
        }

    @staticmethod
    def get_license():
        return open('../modules/shairport-sync/LICENSES').read()
